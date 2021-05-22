# -*- coding: utf-8 -*-

"""Textual preprocessing components.
"""
import re
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime
from itertools import chain
from typing import List, Tuple, Dict

from omoide import core
from omoide.core import constants
from omoide.use_cases.makemigrations.class_all_objects import AllObjects
from omoide.use_cases.makemigrations.class_relocation import Relocation


def preprocess_source(source: str, uuid_master: core.UUIDMaster) -> str:
    """Convert template of the sources file into renderable one.

    Here we're substituting variables and extending contents.
    """
    source = apply_variables(source, uuid_master)
    source = apply_global_variables(source)
    return source


def apply_variables(source: str, uuid_master: core.UUIDMaster) -> str:
    """Substitute variables in sources text."""
    variables = re.findall(constants.UUID_PATTERN, source)

    for variable in set(variables):
        variable_uuid = uuid_master.get_uuid_for_variable(variable)
        source = source.replace(variable, variable_uuid)

    return source


def apply_global_variables(source: str,
                           today: str = str(datetime.now().date())) -> str:
    """Substitute global variables in the sources text."""
    output = source.replace('$today', today)
    return output


def extract_realms(source_dict: dict) -> List[core.Realm]:
    """Create instances of Realm from sources file."""
    instances = []
    entries = source_dict.get('realms', [])

    for entry in entries:
        permissions = frozenset(entry.pop('permissions', []))
        instance = core.Realm(permissions=permissions, **entry)
        instances.append(instance)

    return instances


def extract_themes(source_dict: dict) \
        -> Tuple[List[core.Theme], List[core.ImplicitTag], List[core.Synonym]]:
    """Create instances of Theme from sources file.

    Also generates Implicit tags and Synonyms,
    that does not belong to any theme.
    """
    implicit_tags: Dict[str, List[core.ImplicitTag]] = defaultdict(list)
    entries_implicit_tags = source_dict.get('implicit_tags', [])
    for entry in entries_implicit_tags:
        values = frozenset(entry.pop('values', []))
        tag = core.ImplicitTag(values=values, **entry)
        implicit_tags[tag.theme_uuid].append(tag)

    synonyms: Dict[str, List[core.Synonym]] = defaultdict(list)
    entries_synonyms = source_dict.get('synonyms', [])
    for entry in entries_synonyms:
        values = frozenset(entry.pop('values', []))
        tag = core.Synonym(values=values, **entry)
        synonyms[tag.theme_uuid].append(tag)

    themes: List[core.Theme] = []
    entries_themes = source_dict.get('themes', [])
    for entry in entries_themes:
        uuid = entry.pop('uuid')
        permissions = frozenset(entry.get('permissions', []))
        _implicit_tags = frozenset(implicit_tags.pop(uuid, []))
        _synonyms = frozenset(synonyms.pop(uuid, []))
        theme = core.Theme(
            uuid=uuid,
            permissions=permissions,
            implicit_tags=_implicit_tags,
            synonyms=_synonyms,
            **entry
        )
        themes.append(theme)

    return (
        themes,
        list(chain(*implicit_tags.values())),
        list(chain(*synonyms.values()))
    )


def extract_groups_and_metas(source_folder: str, content_folder: str,
                             source_dict: dict,
                             filesystem: core.Filesystem,
                             renderer: core.Renderer,
                             uuid_master: core.UUIDMaster) \
        -> Tuple[List[core.Group], List[core.Meta], List[Relocation]]:
    """Create instances of Group from sources file.

    Also generates Meta objects,
    that does not belong to any group.
    """
    groups = []
    metas = []
    relocations = []

    entries_groups = source_dict.get('groups', [])
    for entry in entries_groups:
        group_path = entry.pop('path')
        permissions = frozenset(entry.pop('permissions', []))

        group = core.Group(permissions=permissions, **entry)
        new_metas, new_relocations = handle_group_metas(source_folder,
                                                        content_folder,
                                                        group_path,
                                                        group,
                                                        filesystem,
                                                        renderer,
                                                        uuid_master)
        group.members = [x.uuid for x in new_metas]
        metas.extend(new_metas)
        relocations.extend(new_relocations)
        groups.append(group)

    entries_metas = source_dict.get('metas', [])
    for entry in entries_metas:
        metas_path = entry.pop('path')
        entry.pop('uuid', None)  # if user entered it; we do not use it
        permissions = frozenset(entry.pop('permissions', []))

        meta_template = core.Meta(permissions=permissions, **entry)
        new_metas, new_relocations = handle_no_group_metas(source_folder,
                                                           metas_path,
                                                           meta_template,
                                                           filesystem,
                                                           renderer,
                                                           uuid_master)
        metas.extend(new_metas)
        relocations.extend(new_relocations)

    return groups, metas, relocations


def handle_group_metas(root: str, content_folder: str, path: str,
                       group: core.Group,
                       filesystem: core.Filesystem,
                       renderer: core.Renderer,
                       uuid_master: core.UUIDMaster) \
        -> Tuple[List[core.Meta], List[Relocation]]:
    """Instantiate all metas in current group."""
    metas: List[core.Meta] = []
    relocations: List[Relocation] = []
    ordering = 1

    for filename in filesystem.listdir(filesystem.join(root, path)):
        full_path = filesystem.join(root, path, filename)
        name, extension = filesystem.split_extension(filename)
        media_info = renderer.analyze(full_path, extension)

        if not media_info:
            continue

        new_meta = core.Meta(
            uuid=uuid_master.generate_uuid_meta(),
            realm_uuid=group.realm_uuid,
            theme_uuid=group.theme_uuid,
            group_uuid=group.uuid,
            original_filename=name,
            original_extension=extension,
            ordering=ordering,
            registered_on=group.registered_on,
            registered_by=group.registered_by,
            author=group.author,
            author_url=group.author_url,
            origin_url=group.origin_url,
            comment=group.comment,
            hierarchy=group.hierarchy,
            **media_info,
        )
        ordering += 1
        metas.append(new_meta)

        relocations.append(Relocation(
            uuid=new_meta.uuid,
            realm_uuid=new_meta.realm_uuid,
            theme_uuid=new_meta.theme_uuid,
            group_uuid=new_meta.group_uuid,
            source_path=filesystem.absolute(full_path),
            width=new_meta.width,
            height=new_meta.height,
            operation_type='copy',
        ))

        for width, height in [
            (min(new_meta.width, 1024), min(new_meta.height, 1024)),
            (min(new_meta.width, 384), min(new_meta.height, 384))
        ]:
            relocations.append(Relocation(
                uuid=new_meta.uuid,
                realm_uuid=new_meta.realm_uuid,
                theme_uuid=new_meta.theme_uuid,
                group_uuid=new_meta.group_uuid,
                source_path=filesystem.absolute(full_path),
                width=width,
                height=height,
                operation_type='resize',
            ))

    return metas, relocations


def handle_no_group_metas(root: str, path: str, meta_template: core.Meta,
                          filesystem: core.Filesystem,
                          renderer: core.Renderer,
                          uuid_master: core.UUIDMaster) \
        -> Tuple[List[core.Meta], List[Relocation]]:
    """Instantiate all metas without actual group."""
    metas: List[core.Meta] = []
    relocations: List[Relocation] = []
    addition = {
        key: value for key, value in asdict(meta_template).items()
        if value
    }

    for filename in filesystem.listdir(filesystem.join(root, path)):
        full_path = filesystem.join(root, path, filename)
        name, extension = filesystem.split_extension(filename)
        media_info = renderer.analyze(full_path, extension)

        if not media_info:
            continue

        outer_info = {**addition, **media_info}

        new_meta = core.Meta(
            uuid=uuid_master.generate_uuid_meta(),
            original_filename=name,
            original_extension=extension,
            **outer_info,
        )
        metas.append(new_meta)

        relocations.append(Relocation(
            uuid=new_meta.uuid,
            realm_uuid=new_meta.realm_uuid,
            theme_uuid=new_meta.theme_uuid,
            group_uuid=new_meta.group_uuid,
            source_path=filesystem.absolute(full_path),
            width=new_meta.width,
            height=new_meta.height,
            operation_type='copy',
        ))

        for width, height in [
            (min(new_meta.width, 1024), min(new_meta.height, 1024)),
            (min(new_meta.width, 384), min(new_meta.height, 384))
        ]:
            relocations.append(Relocation(
                uuid=new_meta.uuid,
                realm_uuid=new_meta.realm_uuid,
                theme_uuid=new_meta.theme_uuid,
                group_uuid=new_meta.group_uuid,
                source_path=filesystem.absolute(full_path),
                width=width,
                height=height,
                operation_type='resize',
            ))

    return metas, relocations


def instantiate_from_source(current_source_folder: str,
                            content_path: str,
                            source_dict: dict,
                            uuid_master: core.UUIDMaster,
                            filesystem: core.Filesystem,
                            renderer: core.Renderer) -> AllObjects:
    """Make instances from sources file."""
    realms = extract_realms(source_dict)
    themes, implicit_tags, synonyms = extract_themes(source_dict)
    groups, metas, relocations = extract_groups_and_metas(
        current_source_folder,
        content_path,
        source_dict,
        filesystem,
        renderer,
        uuid_master,
    )
    return AllObjects(
        realms=realms,
        themes=themes,
        groups=groups,
        implicit_tags=implicit_tags,
        synonyms=synonyms,
        metas=metas,
        relocations=relocations,
    )
