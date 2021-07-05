# -*- coding: utf-8 -*-

"""Make migrations.
"""
import json
from typing import Any, Dict, List

import omoide.files.constants
from omoide import core
from omoide.files.operations import drop_files_before_making_migrations
from omoide.use_cases import commands
from omoide.use_cases.unite import identity, saving
from omoide.use_cases.unite import preprocessing
from omoide.use_cases.make_relocations.class_relocation import Relocation


def act(command: commands.UniteCommand, filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Create migrations for all trunks."""
    filenames_to_delete = {
        omoide.files.constants.UNIT_FILENAME,
        omoide.files.constants.MIGRATION_FILENAME,
        omoide.files.constants.RELOCATION_FILENAME,
    }
    drop_files_before_making_migrations(command,
                                        filenames_to_delete,
                                        filesystem,
                                        stdout)

    router = core.Router()
    identity_master = core.IdentityMaster()
    uuid_master = core.UUIDMaster()
    renderer = core.Renderer()

    identity.gather_existing_identities(command.sources_folder,
                                        router,
                                        identity_master,
                                        uuid_master,
                                        filesystem)

    total_new_migrations = 0
    for trunk in filesystem.list_folders(command.sources_folder):

        if command.trunk != 'all' and command.trunk != trunk:
            continue

        trunk_folder = filesystem.join(command.sources_folder, trunk)
        for leaf in filesystem.list_folders(trunk_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(trunk_folder, leaf)
            make_migrations_for_single_leaf(
                source_folder=command.sources_folder,
                content_folder=command.content_folder,
                trunk=trunk,
                leaf=leaf,
                leaf_folder=leaf_folder,
                router=router,
                identity_master=identity_master,
                uuid_master=uuid_master,
                renderer=renderer,
                filesystem=filesystem,
                stdout=stdout,
            )
            total_new_migrations += 1

    return total_new_migrations


def make_migrations_for_single_leaf(
        source_folder: str, content_folder: str,
        trunk: str, leaf: str, leaf_folder: str,
        router: core.Router,
        identity_master: core.IdentityMaster,
        uuid_master: core.UUIDMaster,
        renderer: core.Renderer,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> None:
    """Create all migration resources for a single folder."""
    stdout.print(f'Creating migrations for {leaf_folder}')

    source_file_path = filesystem.join(leaf_folder,
                                       omoide.files.constants.SOURCE_FILENAME)

    if filesystem.not_exists(source_file_path):
        stdout.yellow(f'Source file does not exist: {source_file_path}')
        return

    update_file = make_update_file(
        trunk,
        leaf,
        leaf_folder,
        router,
        identity_master,
        uuid_master,
        filesystem,
        renderer
    )

    update_file_path = filesystem.join(leaf_folder,
                                       omoide.files.constants.UNIT_FILENAME)

    filesystem.write_json(update_file_path, update_file)
    stdout.yellow(f'Created update file: {update_file_path}')

    relocations = make_migrations_from_update_file(update_file,
                                                   trunk,
                                                   leaf,
                                                   source_folder,
                                                   content_folder,
                                                   router,
                                                   filesystem)

    relocations_path = saving.save_relocations(
        leaf_folder=leaf_folder,
        relocations=relocations,
        filesystem=filesystem,
    )
    stdout.yellow(f'Created relocations path: {relocations_path}')


def make_update_file(trunk: str, leaf: str, leaf_folder: str,
                     router: core.Router,
                     identity_master: core.IdentityMaster,
                     uuid_master: core.UUIDMaster,
                     filesystem: core.Filesystem,
                     renderer: core.Renderer) -> Dict[str, Any]:
    """Combine all updates in big JSON file."""
    source_file_path = filesystem.join(leaf_folder,
                                       omoide.files.constants.SOURCE_FILENAME)
    source_raw_text = filesystem.read_file(source_file_path)
    source_text = preprocessing.preprocess_source(source_raw_text, trunk, leaf)
    source = json.loads(source_text)

    update = {
        'variables': {},

        'realms': [],
        'themes': [],
        'groups': [],
        'metas': [],
        'users': [],

        'permissions_realm': [],
        'permissions_themes': [],
        'permissions_groups': [],
        'permissions_metas': [],
        'permissions_users': [],

        'tags_realms': [],
        'tags_themes': [],
        'tags_groups': [],
        'tags_metas': [],

        'synonyms': [],
        'implicit_tags': [],
    }
    preprocessing.preprocess_realms(source, update, router,
                                    identity_master, uuid_master)
    preprocessing.preprocess_themes(source, update, router,
                                    identity_master, uuid_master)
    preprocessing.preprocess_groups(source, update, router, identity_master,
                                    uuid_master, filesystem, leaf_folder,
                                    renderer)
    preprocessing.preprocess_no_group_metas(source, update, router,
                                            identity_master,
                                            uuid_master, filesystem,
                                            leaf_folder, renderer)
    preprocessing.preprocess_users(source, update,
                                   identity_master, uuid_master)

    used_variables = identity_master.to_dict()
    update['variables'].update(used_variables)
    identity_master.freeze()

    return update


def make_migrations_from_update_file(update: Dict[str, Any],
                                     trunk: str,
                                     leaf: str,
                                     source_folder: str,
                                     content_folder: str,
                                     router: core.Router,
                                     filesystem: core.Filesystem) \
        -> List[Relocation]:
    """Create SQL migrations and relocations."""
    relocations = []

    for meta in update.get('metas', []):
        make_relocations_for_one_meta(meta,
                                      trunk,
                                      leaf,
                                      source_folder,
                                      content_folder, relocations, router,
                                      filesystem)

    return relocations


def make_relocations_for_one_meta(meta: dict,
                                  trunk: str,
                                  leaf: str,
                                  source_folder: str,
                                  content_folder: str,
                                  relocations: List[Relocation],
                                  router: core.Router,
                                  filesystem: core.Filesystem):
    uuid = meta['uuid']
    realm_uuid = meta['_realm_uuid']
    theme_uuid = meta['_theme_uuid']
    group_uuid = meta['group_uuid']
    filename = meta['original_filename']
    ext = meta['original_extension']

    path_from = filesystem.join(
        source_folder,
        trunk,
        leaf,
        router.get_route(realm_uuid),
        router.get_route(theme_uuid),
        router.get_route(group_uuid),
        f'{filename}.{ext}',
    )

    path_to = filesystem.join(
        content_folder,
        router.get_route(realm_uuid),
        router.get_route(theme_uuid),
        router.get_route(group_uuid),
        f'{uuid}.{ext}'
    )

    new_relocation = Relocation(
        uuid=uuid,
        path_from=path_from,
        path_to=path_to,
        width=meta['width'],
        height=meta['height'],
        operation_type='copy',
    )
    relocations.append(new_relocation)

    for (width, height) in omoide.files.constants.COMPRESS_TO:
        new_relocation = Relocation(
            uuid=uuid,
            path_from=path_from,
            path_to=path_to,
            width=width,
            height=height,
            operation_type='scale',
        )
        relocations.append(new_relocation)


if __name__ == '__main__':
    _command = commands.UniteCommand(
        trunk='all',
        leaf='migration_1',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
