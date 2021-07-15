# -*- coding: utf-8 -*-

"""Textual preprocessing components.
"""
import re
from typing import Tuple

from omoide import constants
from omoide import core
from omoide import use_cases


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


def preprocess_realms(source: dict, unit: dict, router: use_cases.Router,
                      identity_master: use_cases.IdentityMaster,
                      uuid_master: use_cases.UUIDMaster) -> None:
    """Extend realms body."""
    realms = source.pop('realms', [])
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    for realm in realms:
        realm_uuid = identity_master.get_realm_uuid(realm['uuid'], uuid_master)

        for tag in realm.pop('tags', []):
            new_tag = {
                'revision': revision,
                'last_update': now,
                'realm_uuid': realm_uuid,
                'value': tag,
            }
            unit['tags_realms'].append(new_tag)

        for permission in realm.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'realm_uuid': realm_uuid,
                'value': permission,
            }
            unit['permissions_realm'].append(new_permission)

        new_realm = {
            'revision': revision,
            'last_update': now,
            **realm,
            'uuid': realm_uuid,
        }
        unit['realms'].append(new_realm)
        router.register_route(realm_uuid, new_realm['route'])


def preprocess_themes(source: dict, unit: dict, router: use_cases.Router,
                      identity_master: use_cases.IdentityMaster,
                      uuid_master: use_cases.UUIDMaster) -> None:
    """Extend themes body."""
    themes = source.pop('themes', [])
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

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
            unit['synonyms'].append(new_synonym)

        for implicit_tag in theme.pop('implicit_tags', []):
            new_implicit_tag = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': implicit_tag,
            }
            unit['implicit_tags'].append(new_implicit_tag)

        for tag in theme.pop('tags', []):
            new_tag = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': tag,
            }
            unit['tags_themes'].append(new_tag)

        for permission in theme.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'theme_uuid': theme_uuid,
                'value': permission,
            }
            unit['permissions_themes'].append(new_permission)

        new_theme = {
            'revision': revision,
            'last_update': now,
            **theme,
            'uuid': theme_uuid,
            'realm_uuid': realm_uuid,
        }
        unit['themes'].append(new_theme)
        router.register_route(theme_uuid, new_theme['route'])


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


def preprocess_users(source: dict, unit: dict,
                     identity_master: use_cases.IdentityMaster,
                     uuid_master: use_cases.UUIDMaster) -> None:
    """Extend users body."""
    users = source.pop('users', [])
    revision = use_cases.get_revision_number()
    now = use_cases.get_now()

    for user in users:
        user_uuid = identity_master.get_user_uuid(user['uuid'], uuid_master)

        for permission in user.pop('permissions', []):
            new_permission = {
                'revision': revision,
                'last_update': now,
                'user_uuid': user_uuid,
                'value': permission,
            }
            unit['permissions_users'].append(new_permission)

        new_user = {
            'revision': revision,
            'last_update': now,
            **user,
            'uuid': user_uuid,
        }
        unit['users'].append(new_user)
