# -*- coding: utf-8 -*-

"""Textual preprocessing components.
"""
import re
from typing import Union, List, Type

from omoide import constants
from omoide import core
from omoide import use_cases
from omoide.use_cases import unite
from omoide.use_cases.common import transient
from omoide.use_cases.unite import ephemeral
from omoide.use_cases.unite import persistent

CAST_TYPES = Union[
    transient.TagRealm,
    transient.TagTheme,
    transient.TagGroup,
    transient.TagMeta,
    transient.PermissionRealm,
    transient.PermissionTheme,
    transient.PermissionGroup,
    transient.PermissionMeta,
    transient.PermissionUser,
    transient.SynonymValue,
    transient.ImplicitTagValue,
]


def preprocess_source(source: str, branch: str, leaf: str) -> str:
    """Convert template of the sources file into renderable one.

    Here we're substituting variables and extending contents.
    """
    source = apply_global_variables(source)
    source = extend_variable_names(source, branch, leaf)
    return source


def extend_variable_names(source: str, branch: str, leaf: str) -> str:
    """Turn local variable names into global ones.

    >>> extend_variable_names('and $r_1 variable', 'X', 'Y')
    'and $X.Y.r_1 variable'
    """
    variables = re.findall(constants.UUID_VARIABLE_PATTERN, source)

    for variable in set(variables):
        without_sign = variable[1:]
        extended = f'{constants.VARIABLE_SIGN}{branch}.{leaf}.{without_sign}'
        source = source.replace(variable, extended)

    return source


def apply_global_variables(source: str) -> str:
    """Substitute global variables in the sources text."""
    source = source.replace('$today', persistent.get_today())
    source = source.replace('$now', persistent.get_now())
    return source


def cast_all(unit: transient.Unit, unit_field: str, entity_field: str,
             sequence: List[str], target_type: Type[CAST_TYPES], **kwargs):
    """Conversion of a collection of simple textual fields."""
    attribute = getattr(unit, unit_field)

    for value in sequence:
        additional = {entity_field: value, **kwargs}
        new_instance = target_type(
            revision=persistent.get_revision(),
            last_update=persistent.get_now(),
            **additional
        )
        attribute.append(new_instance)


def do_realms(source: ephemeral.Source,
              unit: transient.Unit,
              router: unite.Router,
              identity_master: unite.IdentityMaster,
              uuid_master: unite.UUIDMaster) -> None:
    """Construct transient entities from ephemeral ones."""
    for ep_realm in source.realms:
        realm_uuid = identity_master.get_realm_uuid(ep_realm.uuid, uuid_master)

        cast_all(unit, 'tags_realms', 'value',
                 ep_realm.tags, transient.TagRealm,
                 realm_uuid=realm_uuid)

        cast_all(unit, 'permissions_realm', 'value',
                 ep_realm.permissions, transient.PermissionRealm,
                 realm_uuid=realm_uuid)

        tr_realm = transient.Realm(revision=persistent.get_revision(),
                                   last_update=persistent.get_now(),
                                   uuid=realm_uuid,
                                   route=ep_realm.route,
                                   label=ep_realm.label)
        unit.realms.append(tr_realm)

        router.register_route(realm_uuid, tr_realm.route)


def do_themes(source: ephemeral.Source,
              unit: transient.Unit,
              router: unite.Router,
              identity_master: unite.IdentityMaster,
              uuid_master: unite.UUIDMaster) -> None:
    """Construct transient entities from ephemeral ones."""
    revision = persistent.get_revision()
    now = persistent.get_now()

    for ep_theme in source.themes:
        realm_uuid = identity_master.get_realm_uuid(
            ep_theme.realm_uuid, uuid_master)
        theme_uuid = identity_master.get_theme_uuid(
            ep_theme.uuid, uuid_master)

        for ep_synonym in ep_theme.synonyms:
            s_uuid = identity_master.get_synonym_uuid(
                ep_synonym.uuid, uuid_master)

            ephemeral.ensure_equal(ep_synonym.theme_uuid, ep_theme.uuid)
            tr_synonym = transient.Synonym(revision=revision,
                                           last_update=now,
                                           uuid=s_uuid,
                                           theme_uuid=theme_uuid,
                                           label=ep_synonym.label)
            unit.synonyms.append(tr_synonym)

            cast_all(unit, 'synonyms_values', 'value',
                     ep_synonym.values, transient.SynonymValue,
                     synonym_uuid=s_uuid)

        for ep_itag in ep_theme.implicit_tags:
            itag_uuid = identity_master.get_implicit_tag_uuid(
                ep_itag.uuid, uuid_master)

            tr_implicit_tag = transient.ImplicitTag(revision=revision,
                                                    last_update=now,
                                                    uuid=itag_uuid,
                                                    theme_uuid=theme_uuid,
                                                    label=ep_itag.label)
            unit.implicit_tags.append(tr_implicit_tag)

            cast_all(unit, 'implicit_tags_values', 'value',
                     ep_itag.values, transient.ImplicitTagValue,
                     implicit_tag_uuid=itag_uuid)

        cast_all(unit, 'tags_themes', 'value',
                 ep_theme.tags, transient.TagTheme,
                 theme_uuid=theme_uuid)

        cast_all(unit, 'permissions_themes', 'value',
                 ep_theme.permissions, transient.PermissionTheme,
                 theme_uuid=theme_uuid)

        tr_theme = transient.Theme(revision=revision,
                                   last_update=now,
                                   uuid=theme_uuid,
                                   realm_uuid=realm_uuid,
                                   route=ep_theme.route,
                                   label=ep_theme.label)
        unit.themes.append(tr_theme)

        router.register_route(theme_uuid, tr_theme.route)


def do_groups(source: ephemeral.Source,
              unit: transient.Unit,
              router: unite.Router,
              identity_master: unite.IdentityMaster,
              uuid_master: unite.UUIDMaster,
              filesystem: core.Filesystem,
              leaf_folder: str,
              renderer: use_cases.Renderer) -> None:
    """Construct transient entities from ephemeral ones."""
    for ep_group in source.groups:
        group_uuid = identity_master.get_group_uuid(ep_group.uuid,
                                                    uuid_master)
        theme_uuid = identity_master.get_theme_uuid(ep_group.theme_uuid,
                                                    uuid_master)

        cast_all(unit, 'tags_groups', 'value',
                 ep_group.tags, transient.TagGroup,
                 group_uuid=group_uuid)

        cast_all(unit, 'permissions_groups', 'value',
                 ep_group.permissions, transient.PermissionGroup,
                 group_uuid=group_uuid)

        attributes = ep_group.dict()
        attributes.update({
            'revision': persistent.get_revision(),
            'last_update': persistent.get_now(),
            'uuid': group_uuid,
            'theme_uuid': theme_uuid,
        })

        tr_group = transient.Group(**attributes)
        unit.groups.append(tr_group)
        router.register_route(group_uuid, tr_group.route)

        if ep_group.route != constants.NO_GROUP:
            preprocess_group_meta_pack(
                unit,
                leaf_folder,
                ep_group,
                uuid_master,
                identity_master,
                filesystem,
                renderer,
                router
            )


def do_no_group_metas(source: ephemeral.Source,
                      unit: transient.Unit,
                      router: unite.Router,
                      identity_master: unite.IdentityMaster,
                      uuid_master: unite.UUIDMaster,
                      filesystem: core.Filesystem,
                      leaf_folder: str,
                      renderer: use_cases.Renderer) -> None:
    """Construct transient entities from ephemeral ones."""
    for meta_pack in source.metas:
        preprocess_no_group_meta_pack(unit, leaf_folder, meta_pack,
                                      router, identity_master, uuid_master,
                                      filesystem, renderer)


def preprocess_group_meta_pack(unit: transient.Unit,
                               leaf_folder: str,
                               group: ephemeral.Group,
                               uuid_master: unite.UUIDMaster,
                               identity_master: unite.IdentityMaster,
                               filesystem: core.Filesystem,
                               renderer: use_cases.Renderer,
                               router: unite.Router) -> None:
    """Construct transient entities from ephemeral ones."""
    realm_uuid = identity_master.get_realm_uuid(
        group.realm_uuid, uuid_master, strict=True)
    theme_uuid = identity_master.get_theme_uuid(
        group.theme_uuid, uuid_master, strict=True)
    group_uuid = identity_master.get_group_uuid(
        group.uuid, uuid_master, strict=True)

    realm_route = router.get_route(realm_uuid)
    theme_route = router.get_route(theme_uuid)

    full_path = filesystem.join(leaf_folder, realm_route,
                                theme_route, group.route)

    filenames = []
    for filename in filesystem.list_files(full_path):
        name, extension = filesystem.split_extension(filename)
        if not renderer.is_known_media(extension):
            continue

        filenames.append((name, extension))

    uuids = [uuid_master.generate_uuid_meta() for _ in range(len(filenames))]
    uuids.sort()

    total = len(uuids)

    for i, ((name, ext), uuid) in enumerate(zip(filenames, uuids), start=1):
        file_path = filesystem.join(full_path, f'{name}.{ext}')
        media_info = renderer.analyze(file_path, ext)
        meta_uuid = uuid_master.generate_uuid_meta()

        meta_filename = f'{meta_uuid}.{ext}'
        common = f'{realm_route}/{theme_route}/{group.route}/{meta_filename}'

        path_to_content = f'/content/{common}'
        path_to_preview = f'/preview/{common}'
        path_to_thumbnail = f'/thumbnails/{common}'

        if total == 1:
            _previous = ''
            _next = ''

        elif i == 1 and i < total:
            _previous = ''
            _next = uuids[i]

        elif i == total:
            _previous = uuids[i - 2]
            _next = ''

        else:
            _previous = uuids[i - 2]
            _next = uuids[i]

        tr_meta = transient.Meta(
            revision=persistent.get_revision(),
            last_update=persistent.get_now(),
            uuid=meta_uuid,
            realm_uuid=realm_uuid,
            theme_uuid=theme_uuid,
            group_uuid=group_uuid,
            original_filename=name,
            original_extension=ext,
            ordering=i,
            path_to_content=path_to_content,
            path_to_preview=path_to_preview,
            path_to_thumbnail=path_to_thumbnail,
            previous=_previous,
            next=_next,
            **media_info,
            author=group.author,
            author_url=group.author_url,
            origin_url=group.origin_url,
            comment=group.comment,
            hierarchy=group.hierarchy,
        )
        unit.metas.append(tr_meta)

        cast_all(unit, 'tags_metas', 'value',
                 group.tags, transient.TagMeta,
                 meta_uuid=meta_uuid)

        cast_all(unit, 'permissions_metas', 'value',
                 group.permissions, transient.PermissionMeta,
                 meta_uuid=meta_uuid)


def preprocess_no_group_meta_pack(unit: transient.Unit,
                                  leaf_folder: str,
                                  ep_meta: ephemeral.Meta,
                                  router: unite.Router,
                                  identity_master: unite.IdentityMaster,
                                  uuid_master: unite.UUIDMaster,
                                  filesystem: core.Filesystem,
                                  renderer: use_cases.Renderer) -> None:
    """Construct transient entities from ephemeral ones."""
    realm_uuid = identity_master.get_realm_uuid(ep_meta.realm_uuid,
                                                uuid_master, strict=True)
    theme_uuid = identity_master.get_theme_uuid(ep_meta.theme_uuid,
                                                uuid_master, strict=True)
    group_uuid = identity_master.get_group_uuid(ep_meta.group_uuid,
                                                uuid_master, strict=True)

    realm_route = router.get_route(realm_uuid)
    theme_route = router.get_route(theme_uuid)
    group_route = router.get_route(group_uuid)

    full_path = filesystem.join(leaf_folder,
                                realm_route,
                                theme_route,
                                group_route)
    uuids = [
        uuid_master.generate_uuid_meta() for _ in range(len(ep_meta.filenames))
    ]
    uuids.sort()

    for filename, uuid in zip(ep_meta.filenames, uuids):
        name, ext = filesystem.split_extension(filename)
        file_path = filesystem.join(full_path, filename)
        media_info = renderer.analyze(file_path, ext)
        meta_uuid = uuid_master.generate_uuid_meta()

        meta_filename = f'{meta_uuid}.{ext}'
        common = f'{realm_route}/{theme_route}/{group_route}/{meta_filename}'

        path_to_content = f'/content/{common}'
        path_to_preview = f'/preview/{common}'
        path_to_thumbnail = f'/thumbnails/{common}'

        tr_meta = transient.Meta(
            revision=persistent.get_revision(),
            last_update=persistent.get_now(),
            uuid=meta_uuid,
            realm_uuid=realm_uuid,
            theme_uuid=theme_uuid,
            group_uuid=group_uuid,
            original_filename=name,
            original_extension=ext,
            ordering=0,
            path_to_content=path_to_content,
            path_to_preview=path_to_preview,
            path_to_thumbnail=path_to_thumbnail,
            previous='',
            next='',
            **media_info,
            author=ep_meta.author,
            author_url=ep_meta.author_url,
            origin_url=ep_meta.origin_url,
            comment=ep_meta.comment,
            hierarchy=ep_meta.hierarchy,
        )
        unit.metas.append(tr_meta)

        cast_all(unit, 'tags_metas', 'value',
                 ep_meta.permissions, transient.TagMeta,
                 meta_uuid=meta_uuid)

        cast_all(unit, 'permissions_metas', 'value',
                 ep_meta.permissions, transient.PermissionMeta,
                 meta_uuid=meta_uuid)


def do_users(source: ephemeral.Source,
             unit: transient.Unit,
             identity_master: unite.IdentityMaster,
             uuid_master: unite.UUIDMaster) -> None:
    """Construct transient entities from ephemeral ones."""
    for ep_user in source.users:
        user_uuid = identity_master.get_user_uuid(ep_user.uuid, uuid_master)

        cast_all(unit, 'permissions_users', 'value',
                 ep_user.permissions, transient.PermissionUser,
                 user_uuid=user_uuid)

        tr_user = transient.User(revision=persistent.get_revision(),
                                 last_update=persistent.get_now(),
                                 uuid=user_uuid,
                                 name=ep_user.name)
        unit.users.append(tr_user)
