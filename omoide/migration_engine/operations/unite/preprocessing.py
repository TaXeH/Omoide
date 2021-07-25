# -*- coding: utf-8 -*-

"""Textual preprocessing components.
"""
import re
from typing import Union, List, Type, Tuple

from omoide import constants
from omoide import infra
from omoide.migration_engine import classes
from omoide.migration_engine import persistent, transient, ephemeral
from omoide.migration_engine.operations import unite

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


def preprocess_source(text: str, branch: str, leaf: str,
                      identity_master: unite.IdentityMaster,
                      uuid_master: unite.UUIDMaster) -> str:
    """Convert template of the sources file into renderable one.

    Here we're substituting variables and extending contents.
    """
    text = apply_global_variables(text)
    text = generate_variables(text, branch, leaf, identity_master, uuid_master)
    text = apply_variables(text, identity_master)
    return text


def apply_global_variables(source: str) -> str:
    """Substitute global variables in the source text."""
    source = source.replace('$today', persistent.get_today())
    source = source.replace('$now', persistent.get_now())
    return source


def generate_variables(text: str, branch: str, leaf: str,
                       identity_master: unite.IdentityMaster,
                       uuid_master: unite.UUIDMaster) -> str:
    """Substitute UUID variables in the source text."""
    pattern = re.compile(constants.UUID_MAKE_VARIABLE_PATTERN, re.IGNORECASE)

    _to_replace: List[Tuple[str, str]] = []

    for match in re.finditer(pattern, text):
        uuid_type, variable_name = match.groups()
        variable_value = identity_master.generate_value(
            branch=branch,
            leaf=leaf,
            uuid_type=uuid_type,
            variable=variable_name,
            uuid_master=uuid_master,
        )
        _to_replace.append((text[match.start():match.end()], variable_value))

    for pattern, value in _to_replace:
        text = text.replace(pattern, value)

    return text


def apply_variables(text: str, identity_master: unite.IdentityMaster) -> str:
    """Replace variable names with values."""
    variables = re.findall(constants.UUID_VARIABLE_PATTERN, text)

    for with_sign in set(variables):
        variable_name = with_sign[1:]
        variable_value = identity_master.get_value(variable_name)
        text = text.replace(with_sign, variable_value)

    return text


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
              router: unite.Router) -> None:
    """Construct transient entities from ephemeral ones."""
    for ep_realm in source.realms:
        cast_all(unit, 'tags_realms', 'value',
                 ep_realm.tags, transient.TagRealm,
                 realm_uuid=ep_realm.uuid)

        cast_all(unit, 'permissions_realm', 'value',
                 ep_realm.permissions, transient.PermissionRealm,
                 realm_uuid=ep_realm.uuid)

        tr_realm = transient.Realm(revision=persistent.get_revision(),
                                   last_update=persistent.get_now(),
                                   uuid=ep_realm.uuid,
                                   route=ep_realm.route,
                                   label=ep_realm.label)
        unit.realms.append(tr_realm)

        router.register_route(ep_realm.uuid, tr_realm.route)


def do_themes(source: ephemeral.Source,
              unit: transient.Unit,
              router: unite.Router) -> None:
    """Construct transient entities from ephemeral ones."""
    revision = persistent.get_revision()
    now = persistent.get_now()

    for ep_theme in source.themes:
        for ep_synonym in ep_theme.synonyms:
            ephemeral.assert_equal(ep_synonym.theme_uuid, ep_theme.uuid)
            tr_synonym = transient.Synonym(
                revision=revision,
                last_update=now,
                uuid=ep_synonym.uuid,
                theme_uuid=ep_synonym.theme_uuid,
                label=ep_synonym.label,
            )
            unit.synonyms.append(tr_synonym)

            cast_all(unit, 'synonyms_values', 'value',
                     ep_synonym.values, transient.SynonymValue,
                     synonym_uuid=ep_synonym.uuid)

        for ep_itag in ep_theme.implicit_tags:
            tr_implicit_tag = transient.ImplicitTag(
                revision=revision,
                last_update=now,
                uuid=ep_itag.uuid,
                theme_uuid=ep_itag.theme_uuid,
                label=ep_itag.label,
            )
            unit.implicit_tags.append(tr_implicit_tag)

            cast_all(unit, 'implicit_tags_values', 'value',
                     ep_itag.values, transient.ImplicitTagValue,
                     implicit_tag_uuid=ep_itag.uuid)

        cast_all(unit, 'tags_themes', 'value',
                 ep_theme.tags, transient.TagTheme,
                 theme_uuid=ep_theme.uuid)

        cast_all(unit, 'permissions_themes', 'value',
                 ep_theme.permissions, transient.PermissionTheme,
                 theme_uuid=ep_theme.uuid)

        tr_theme = transient.Theme(
            revision=revision,
            last_update=now,
            uuid=ep_theme.uuid,
            realm_uuid=ep_theme.realm_uuid,
            route=ep_theme.route,
            label=ep_theme.label,
        )
        unit.themes.append(tr_theme)

        router.register_route(tr_theme.uuid, tr_theme.route)


def do_groups(source: ephemeral.Source,
              unit: transient.Unit,
              router: unite.Router,
              identity_master: unite.IdentityMaster,
              uuid_master: unite.UUIDMaster,
              filesystem: infra.Filesystem,
              leaf_folder: str,
              renderer: classes.Renderer) -> None:
    """Construct transient entities from ephemeral ones."""
    for ep_group in source.groups:
        cast_all(unit, 'tags_groups', 'value',
                 ep_group.tags, transient.TagGroup,
                 group_uuid=ep_group.uuid)

        cast_all(unit, 'permissions_groups', 'value',
                 ep_group.permissions, transient.PermissionGroup,
                 group_uuid=ep_group.uuid)

        attributes = ep_group.dict()
        attributes.update({
            'revision': persistent.get_revision(),
            'last_update': persistent.get_now(),
            'uuid': ep_group.uuid,
            'theme_uuid': ep_group.theme_uuid,
        })

        tr_group = transient.Group(**attributes)
        unit.groups.append(tr_group)
        router.register_route(tr_group.uuid, tr_group.route)

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
                      uuid_master: unite.UUIDMaster,
                      filesystem: infra.Filesystem,
                      leaf_folder: str,
                      renderer: classes.Renderer) -> None:
    """Construct transient entities from ephemeral ones."""
    for meta_pack in source.metas:
        preprocess_no_group_meta_pack(unit, leaf_folder, meta_pack,
                                      router, uuid_master,
                                      filesystem, renderer)


def preprocess_group_meta_pack(unit: transient.Unit,
                               leaf_folder: str,
                               group: ephemeral.Group,
                               uuid_master: unite.UUIDMaster,
                               identity_master: unite.IdentityMaster,
                               filesystem: infra.Filesystem,
                               renderer: classes.Renderer,
                               router: unite.Router) -> None:
    """Construct transient entities from ephemeral ones."""
    realm_route = router.get_route(group.realm_uuid)
    theme_route = router.get_route(group.theme_uuid)

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

        path_to_content = (
            f'/{constants.MEDIA_CONTENT_FOLDER_NAME}/{common}'
        )
        path_to_preview = (
            f'/{constants.MEDIA_PREVIEW_FOLDER_NAME}/{common}'
        )
        path_to_thumbnail = (
            f'/{constants.MEDIA_THUMBNAILS_FOLDER_NAME}/{common}'
        )

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
            realm_uuid=group.realm_uuid,
            theme_uuid=group.theme_uuid,
            group_uuid=group.uuid,
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
                                  uuid_master: unite.UUIDMaster,
                                  filesystem: infra.Filesystem,
                                  renderer: classes.Renderer) -> None:
    """Construct transient entities from ephemeral ones."""
    realm_route = router.get_route(ep_meta.realm_uuid)
    theme_route = router.get_route(ep_meta.theme_uuid)
    group_route = router.get_route(ep_meta.group_uuid)

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
            realm_uuid=ep_meta.realm_uuid,
            theme_uuid=ep_meta.theme_uuid,
            group_uuid=ep_meta.group_uuid,
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


def do_users(source: ephemeral.Source, unit: transient.Unit) -> None:
    """Construct transient entities from ephemeral ones."""
    for ep_user in source.users:
        cast_all(unit, 'permissions_users', 'value',
                 ep_user.permissions, transient.PermissionUser,
                 user_uuid=ep_user.uuid)

        tr_user = transient.User(
            revision=persistent.get_revision(),
            last_update=persistent.get_now(),
            uuid=ep_user.uuid,
            name=ep_user.name,
        )
        unit.users.append(tr_user)
