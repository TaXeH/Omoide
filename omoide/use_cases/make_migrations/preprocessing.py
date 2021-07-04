# -*- coding: utf-8 -*-

"""Textual preprocessing components.
"""
import re

from omoide import core
from omoide.core import constants
from omoide.use_cases.make_migrations import identity


def preprocess_source(source: str, trunk: str, leaf: str) -> str:
    """Convert template of the sources file into renderable one.

    Here we're substituting variables and extending contents.
    """
    source = apply_global_variables(source)
    source = extend_variable_names(source, trunk, leaf)
    return source


def extend_variable_names(source: str, trunk: str, leaf: str) -> str:
    """Turn local variable names into global ones.

    >>> extend_variable_names('and $r_1 variable', 'X', 'Y')
    'and $X.Y.r_1 variable'
    """
    variables = re.findall(constants.UUID_VARIABLE_PATTERN, source)

    for variable in set(variables):
        without_sign = variable[1:]
        extended = f'{constants.VARIABLE_SIGN}{trunk}.{leaf}.{without_sign}'
        source = source.replace(variable, extended)

    return source


def apply_global_variables(source: str) -> str:
    """Substitute global variables in the sources text."""
    source = source.replace('$today', identity.get_today())
    source = source.replace('$now', identity.get_now())
    return source


def preprocess_realms(source: dict, update: dict,
                      identity_master: core.IdentityMaster,
                      uuid_master: core.UUIDMaster) -> None:
    """Extend realms body."""
    realms = source.pop('realms', [])
    revision = identity.get_revision_number()
    now = identity.get_now()

    for realm in realms:
        realm_uuid = identity_master.get_realm_uuid(realm['uuid'], uuid_master)

        for tag in realm.pop('tags', []):
            new_tag = {
                'revision': revision,
                'last_update': now,
                'realm_uuid': realm_uuid,
                'value': tag,
            }
            update['tags_realms'].append(new_tag)

        for permission in realm.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'realm_uuid': realm_uuid,
                'value': permission,
            }
            update['permissions_realm'].append(new_permission)

        new_realm = {
            'revision': revision,
            'last_update': now,
            **realm,
            'uuid': realm_uuid,
        }
        update['realms'].append(new_realm)


def preprocess_themes(source: dict, update: dict,
                      identity_master: core.IdentityMaster,
                      uuid_master: core.UUIDMaster) -> None:
    """Extend themes body."""
    themes = source.pop('themes', [])
    revision = identity.get_revision_number()
    now = identity.get_now()

    for theme in themes:
        realm_uuid = identity_master.get_realm_uuid(theme['realm_uuid'],
                                                    uuid_master)
        theme_uuid = identity_master.get_theme_uuid(theme['uuid'], uuid_master)

        for synonym in theme.pop('synonyms', []):
            new_synonym = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': synonym,
            }
            update['synonyms'].append(new_synonym)

        for implicit_tag in theme.pop('implicit_tags', []):
            new_implicit_tag = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': implicit_tag,
            }
            update['implicit_tags'].append(new_implicit_tag)

        for tag in theme.pop('tags', []):
            new_tag = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': tag,
            }
            update['tags_themes'].append(new_tag)

        for permission in theme.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': permission,
            }
            update['permissions_themes'].append(new_permission)

        new_theme = {
            'revision': revision,
            'last_update': now,
            **theme,
            'uuid': theme_uuid,
            'realm_uuid': realm_uuid,
        }
        update['themes'].append(new_theme)


def preprocess_groups(source: dict,
                      update: dict,
                      identity_master: core.IdentityMaster,
                      uuid_master: core.UUIDMaster,
                      filesystem: core.Filesystem,
                      leaf_folder: str,
                      renderer: core.Renderer) -> None:
    """Extend groups body."""
    groups = source.pop('groups', [])
    revision = identity.get_revision_number()
    now = identity.get_now()

    for group in groups:
        group_uuid = identity_master.get_group_uuid(group['uuid'], uuid_master)
        theme_uuid = identity_master.get_theme_uuid(group['theme_uuid'],
                                                    uuid_master)

        for tag in group.pop('tags', []):
            new_tag = {
                'revision': revision,
                'last_update': now,
                'group_uuid': group_uuid,
                'value': tag,
            }
            update['tags_groups'].append(new_tag)

        for permission in group.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'group_uuid': group_uuid,
                'value': permission,
            }
            update['permissions_groups'].append(new_permission)

        new_group = {
            'revision': revision,
            'last_update': now,
            **group,
            'uuid': group_uuid,
            'theme_uuid': theme_uuid,
        }
        update['groups'].append(new_group)

        if group['route'] != '_':
            path = group.pop('route')
            group.pop('uuid', None)
            group.pop('label', None)
            group.pop('theme_uuid', None)
            group['group_uuid'] = group_uuid
            preprocess_single_meta_pack(update, leaf_folder, path,
                                        group, identity_master, uuid_master,
                                        filesystem, renderer)


def preprocess_non_group_metas(source: dict,
                               update: dict,
                               identity_master: core.IdentityMaster,
                               uuid_master: core.UUIDMaster,
                               filesystem: core.Filesystem,
                               leaf_folder: str,
                               renderer: core.Renderer) -> None:
    """Extend metas body."""
    metas = source.pop('metas', [])

    for meta_pack in metas:
        path = 'no_group'
        preprocess_single_meta_pack(update, leaf_folder, path,
                                    meta_pack, identity_master, uuid_master,
                                    filesystem, renderer)


def preprocess_single_meta_pack(update: dict, leaf_folder: str,
                                sub_folder: str, pack: dict,
                                identity_master: core.IdentityMaster,
                                uuid_master: core.UUIDMaster,
                                filesystem: core.Filesystem,
                                renderer: core.Renderer) -> None:
    """Gather basic info on a specific meta."""
    revision = identity.get_revision_number()
    now = identity.get_now()

    group_uuid_variable = pack.pop('group_uuid')
    group_uuid = identity_master.get_group_uuid(group_uuid_variable,
                                                uuid_master)

    tags = pack.pop('tags', [])
    permissions = pack.pop('permissions', [])

    full_path = filesystem.join(leaf_folder, sub_folder)

    filenames = []
    for filename in filesystem.list_files(full_path):
        name, extension = filesystem.split_extension(filename)
        if not renderer.is_known_media(extension):
            continue

        filenames.append((name, extension))

    uuids = [uuid_master.generate_uuid_meta() for _ in range(len(filenames))]
    uuids.sort()

    for i, ((name, ext), uuid) in enumerate(zip(filenames, uuids), start=1):
        file_path = filesystem.join(full_path, f'{name}.{ext}')
        media_info = renderer.analyze(file_path, ext)
        meta_uuid = uuid_master.generate_uuid_meta()

        new_meta = {
            'revision': revision,
            'last_update': now,
            'uuid': meta_uuid,
            'group_uuid': group_uuid,
            'original_filename': name,
            'original_extension': ext,
            'ordering': i,
            **pack,
            **media_info,
        }
        update['metas'].append(new_meta)

        for tag in tags:
            new_tag = {
                'revision': revision,
                'last_update': now,
                'meta_uuid': meta_uuid,
                'value': tag,
            }
            update['tags_metas'].append(new_tag)

        for permission in permissions:
            new_permission = {
                'revision': revision,
                'last_update': now,
                'meta_uuid': meta_uuid,
                'value': permission,
            }
            update['permissions_metas'].append(new_permission)


def preprocess_users(source: dict, update: dict,
                     identity_master: core.IdentityMaster,
                     uuid_master: core.UUIDMaster) -> None:
    """Extend users body."""
    # TODO
