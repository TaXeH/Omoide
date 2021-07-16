# -*- coding: utf-8 -*-

"""Textual preprocessing components.
"""
import re
from typing import Tuple

from omoide import constants
from omoide import core
from omoide import use_cases
from omoide.use_cases.common import ephemeral
from omoide.use_cases.common import transient


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
    source = source.replace('$today', use_cases.get_today())
    source = source.replace('$now', use_cases.get_now())
    return source


def preprocess_realms(source: ephemeral.Source,
                      unit: transient.Unit,
                      router: use_cases.Router,
                      identity_master: use_cases.IdentityMaster,
                      uuid_master: use_cases.UUIDMaster) -> None:
    """Extend realms body."""
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    for ep_realm in source.realms:
        realm_uuid = identity_master.get_realm_uuid(ep_realm.uuid, uuid_master)

        assert len(ep_realm.tags) == len(set(ep_realm.tags))
        for tag_string in ep_realm.tags:
            new_tag = transient.TagRealm(
                revision=revision,
                last_update=now,
                realm_uuid=realm_uuid,
                value=tag_string,
            )
            unit.tags_realms.append(new_tag)

        assert len(ep_realm.permissions) == len(set(ep_realm.permissions))
        for permission_string in ep_realm.permissions:
            new_permission = transient.PermissionRealm(
                revision=revision,
                last_update=now,
                realm_uuid=realm_uuid,
                value=permission_string,
            )
            unit.permissions_realm.append(new_permission)

        new_realm = transient.Realm(
            revision=revision,
            last_update=now,
            uuid=realm_uuid,
            route=ep_realm.route,
            label=ep_realm.label
        )
        unit.realms.append(new_realm)
        router.register_route(realm_uuid, new_realm.route)


def preprocess_themes(source: ephemeral.Source,
                      unit: transient.Unit,
                      router: use_cases.Router,
                      identity_master: use_cases.IdentityMaster,
                      uuid_master: use_cases.UUIDMaster) -> None:
    """Extend themes body."""
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    for ep_theme in source.themes:
        realm_uuid = identity_master.get_realm_uuid(
            ep_theme.realm_uuid, uuid_master)
        theme_uuid = identity_master.get_theme_uuid(
            ep_theme.uuid, uuid_master)

        for synonym in ep_theme.synonyms:
            synonym_uuid = identity_master.get_synonym_uuid(
                synonym.uuid, uuid_master)

            new_synonym = transient.Synonym(
                revision=revision,
                last_update=now,
                uuid=synonym_uuid,
                theme_uuid=theme_uuid,
                label=synonym.label,
            )
            unit.synonyms.append(new_synonym)

            assert len(synonym.values) == len(set(synonym.values))
            for value in synonym.values:
                new_synonym_value = transient.SynonymValue(
                    revision=revision,
                    last_update=now,
                    synonym_uuid=synonym_uuid,
                    value=value,
                )
                unit.synonyms_values.append(new_synonym_value)

        for implicit_tag in ep_theme.implicit_tags:
            implicit_tag_uuid = identity_master.get_implicit_tag_uuid(
                implicit_tag.uuid, uuid_master)

            new_implicit_tag = transient.ImplicitTag(
                revision=revision,
                last_update=now,
                uuid=implicit_tag_uuid,
                theme_uuid=theme_uuid,
                label=implicit_tag.label,
            )
            unit.implicit_tags.append(new_implicit_tag)

            assert len(implicit_tag.values) \
                   == len(set(implicit_tag.values))
            for value in implicit_tag.values:
                new_implicit_tag_value = transient.ImplicitTagValue(
                    revision=revision,
                    last_update=now,
                    implicit_tag_uuid=implicit_tag_uuid,
                    value=value,
                )
                unit.implicit_tags_values.append(new_implicit_tag_value)

        assert len(ep_theme.tags) == len(set(ep_theme.tags))
        for tag in ep_theme.tags:
            new_tag = transient.TagTheme(
                revision=revision,
                last_update=now,
                theme_uuid=theme_uuid,
                value=tag,
            )
            unit.tags_themes.append(new_tag)

        assert len(ep_theme.permissions) == len(set(ep_theme.permissions))
        for permission in ep_theme.permissions:
            new_permission = transient.PermissionTheme(
                revision=revision,
                last_update=now,
                theme_uuid=theme_uuid,
                value=permission,
            )
            unit.permissions_themes.append(new_permission)

        new_theme = transient.Theme(
            revision=revision,
            last_update=now,
            uuid=theme_uuid,
            realm_uuid=realm_uuid,
            route=ep_theme.route,
            label=ep_theme.label,
        )
        unit.themes.append(new_theme)
        router.register_route(theme_uuid, new_theme.route)


def preprocess_groups(source: dict,
                      unit: dict,
                      router: use_cases.Router,
                      identity_master: use_cases.IdentityMaster,
                      uuid_master: use_cases.UUIDMaster,
                      filesystem: core.Filesystem,
                      leaf_folder: str,
                      renderer: use_cases.Renderer) -> None:
    """Extend groups body."""
    groups = source.pop('groups', [])
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

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
            unit['tags_groups'].append(new_tag)

        for permission in group.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'group_uuid': group_uuid,
                'value': permission,
            }
            unit['permissions_groups'].append(new_permission)

        new_group = {
            'revision': revision,
            'last_update': now,
            **group,
            'uuid': group_uuid,
            'theme_uuid': theme_uuid,
        }
        unit['groups'].append(new_group)
        router.register_route(group_uuid, new_group['route'])

        if group['route'] != 'no_group':
            group_route = group.pop('route')
            group.pop('uuid', None)
            group.pop('label', None)
            group.pop('theme_uuid', None)

            realm_route, realm_uuid = _kostyl(theme_uuid, unit, router)
            group['_realm_uuid'] = realm_uuid
            group['_theme_uuid'] = theme_uuid
            theme_route = router.get_route(theme_uuid)
            preprocess_group_meta_pack(
                unit,
                leaf_folder,
                realm_route,
                theme_route,
                group_route,
                group_uuid,
                group,
                uuid_master,
                filesystem,
                renderer,
            )


def _kostyl(theme_uuid, update, router) -> Tuple[str, str]:
    """Find realm route by theme uuid."""
    # FIXME
    for theme in update['themes']:
        if theme['uuid'] == theme_uuid:
            realm_uuid = theme['realm_uuid']
            return router.get_route(realm_uuid), realm_uuid
    raise ValueError


def preprocess_no_group_metas(source: dict,
                              update: dict,
                              router: use_cases.Router,
                              identity_master: use_cases.IdentityMaster,
                              uuid_master: use_cases.UUIDMaster,
                              filesystem: core.Filesystem,
                              leaf_folder: str,
                              renderer: use_cases.Renderer) -> None:
    """Extend metas body."""
    metas = source.pop('metas', [])

    for meta_pack in metas:
        preprocess_no_group_meta_pack(update, leaf_folder, meta_pack,
                                      router, identity_master, uuid_master,
                                      filesystem, renderer)


def preprocess_group_meta_pack(update: dict,
                               leaf_folder: str,
                               realm_route: str,
                               theme_route: str,
                               group_route: str,
                               group_uuid: str,
                               pack: dict,
                               uuid_master: use_cases.UUIDMaster,
                               filesystem: core.Filesystem,
                               renderer: use_cases.Renderer) -> None:
    """Gather basic info on a specific meta."""
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    tags = pack.pop('tags', [])
    permissions = pack.pop('permissions', [])

    full_path = filesystem.join(leaf_folder, realm_route,
                                theme_route, group_route)

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
        common = f'{realm_route}/{theme_route}/{group_route}/{meta_filename}'

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

        new_meta = {
            'revision': revision,
            'last_update': now,
            'uuid': meta_uuid,
            'group_uuid': group_uuid,
            'original_filename': name,
            'original_extension': ext,
            'ordering': i,
            'path_to_content': path_to_content,
            'path_to_preview': path_to_preview,
            'path_to_thumbnail': path_to_thumbnail,
            'previous': _previous,
            'next': _next,
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


def preprocess_no_group_meta_pack(update: dict,
                                  leaf_folder: str,
                                  pack: dict,
                                  router: use_cases.Router,
                                  identity_master: use_cases.IdentityMaster,
                                  uuid_master: use_cases.UUIDMaster,
                                  filesystem: core.Filesystem,
                                  renderer: use_cases.Renderer) -> None:
    """Gather basic info on a specific meta."""
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    realm_uuid = identity_master.get_realm_uuid(pack.pop('_realm_uuid'),
                                                uuid_master, strict=True)
    theme_uuid = identity_master.get_theme_uuid(pack.pop('_theme_uuid'),
                                                uuid_master, strict=True)
    group_uuid = identity_master.get_group_uuid(pack['group_uuid'],
                                                uuid_master, strict=True)
    pack['group_uuid'] = group_uuid
    pack['_realm_uuid'] = realm_uuid
    pack['_theme_uuid'] = theme_uuid

    realm_route = router.get_route(realm_uuid)
    theme_route = router.get_route(theme_uuid)
    group_route = router.get_route(group_uuid)

    tags = pack.pop('tags', [])
    permissions = pack.pop('permissions', [])
    filenames = pack.pop('filenames', [])

    full_path = filesystem.join(leaf_folder,
                                realm_route,
                                theme_route,
                                group_route)
    uuids = [uuid_master.generate_uuid_meta() for _ in range(len(filenames))]
    uuids.sort()

    for filename, uuid in zip(filenames, uuids):
        name, ext = filesystem.split_extension(filename)
        file_path = filesystem.join(full_path, filename)
        media_info = renderer.analyze(file_path, ext)
        meta_uuid = uuid_master.generate_uuid_meta()

        meta_filename = f'{meta_uuid}.{ext}'
        common = f'{realm_route}/{theme_route}/{group_route}/{meta_filename}'

        path_to_content = f'/content/{common}'
        path_to_preview = f'/preview/{common}'
        path_to_thumbnail = f'/thumbnails/{common}'

        new_meta = {
            'revision': revision,
            'last_update': now,
            'uuid': meta_uuid,
            'group_uuid': group_uuid,
            'original_filename': name,
            'original_extension': ext,
            'ordering': 0,
            'path_to_content': path_to_content,
            'path_to_preview': path_to_preview,
            'path_to_thumbnail': path_to_thumbnail,
            'previous': '',
            'next': '',
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


def preprocess_users(source: ephemeral.Source,
                     unit: transient.Unit,
                     identity_master: use_cases.IdentityMaster,
                     uuid_master: use_cases.UUIDMaster) -> None:
    """Extend users body."""
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    for ep_user in source.users:
        user_uuid = identity_master.get_user_uuid(ep_user.uuid, uuid_master)

        assert len(ep_user.permissions) == len(set(ep_user.permissions))
        for permission in ep_user.permissions:
            new_permission = transient.PermissionUser(
                revision=revision,
                last_update=now,
                user_uuid=user_uuid,
                value=permission,
            )
            unit.permissions_users.append(new_permission)

        new_user = transient.User(
            revision=revision,
            last_update=now,
            uuid=user_uuid,
            name=ep_user.name,
        )
        unit.users.append(new_user)
