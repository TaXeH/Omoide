# -*- coding: utf-8 -*-

"""Make migrations.
"""
import json
from typing import Any, Dict, Tuple, List

import omoide.files.constants
from omoide import core
from omoide.files.operations import drop_files_before_making_migrations
from omoide.use_cases import commands
from omoide.use_cases.make_migrations import identity
from omoide.use_cases.make_migrations import preprocessing
from omoide.use_cases.make_migrations.class_relocation import Relocation
from omoide.use_cases.make_migrations.class_sql import SQL


def act(command: commands.MakeMigrationsCommand, filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Create migrations for all trunks."""
    filenames_to_delete = {
        omoide.files.constants.UPDATE_FILENAME,
        omoide.files.constants.MIGRATION_FILENAME,
        omoide.files.constants.RELOCATION_FILENAME,
    }
    drop_files_before_making_migrations(command.sources_folder,
                                        filenames_to_delete,
                                        filesystem,
                                        stdout)

    identity_master = core.IdentityMaster()
    uuid_master = core.UUIDMaster()
    renderer = core.Renderer()

    identity.gather_existing_identities(command.sources_folder,
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
                trunk=trunk,
                leaf=leaf,
                leaf_folder=leaf_folder,
                content_folder=command.content_folder,
                identity_master=identity_master,
                uuid_master=uuid_master,
                renderer=renderer,
                filesystem=filesystem,
                stdout=stdout,
            )
            total_new_migrations += 1

    return total_new_migrations


def make_migrations_for_single_leaf(trunk: str, leaf: str, leaf_folder: str,
                                    content_folder: str,
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

    update_file = make_update_file(trunk, leaf, leaf_folder, identity_master,
                                   uuid_master, filesystem, renderer)

    update_file_path = filesystem.join(leaf_folder,
                                       omoide.files.constants.UPDATE_FILENAME)

    filesystem.write_json(update_file_path, update_file)
    stdout.yellow(f'Created update file: {update_file_path}')

    # migrations, relocations = make_migrations_from_update_file(update_file,
    #                                                            content_folder,
    #                                                            renderer,
    #                                                            filesystem,
    #                                                            stdout)
    # migrations_path = saving.save_migrations(
    #     leaf_folder=leaf_folder,
    #     migrations=migrations,
    #     filesystem=filesystem,
    # )
    # stdout.yellow(f'Created migrations file: {migrations_path}')
    #
    # relocations_path = saving.save_relocations(
    #     leaf_folder=leaf_folder,
    #     relocations=relocations,
    #     filesystem=filesystem,
    # )
    # stdout.yellow(f'Created relocations path: {relocations_path}')


def make_update_file(trunk: str, leaf: str, leaf_folder: str,
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
    preprocessing.preprocess_realms(source, update,
                                    identity_master, uuid_master)
    preprocessing.preprocess_themes(source, update,
                                    identity_master, uuid_master)
    preprocessing.preprocess_groups(source, update, identity_master,
                                    uuid_master, filesystem, leaf_folder,
                                    renderer)
    preprocessing.preprocess_non_group_metas(source, update, identity_master,
                                             uuid_master, filesystem,
                                             leaf_folder, renderer)
    preprocessing.preprocess_users(source, update,
                                   identity_master, uuid_master)

    update['variables'].update(identity_master.to_dict())

    return update


def make_migrations_from_update_file(update: Dict[str, Any],
                                     content_folder: str,
                                     renderer: core.Renderer,
                                     filesystem: core.Filesystem,
                                     stdout: core.STDOut) \
        -> Tuple[List[SQL], List[Relocation]]:
    """Create SQL migrations and relocations."""
    return [], []


if __name__ == '__main__':
    _command = commands.MakeMigrationsCommand(
        trunk='all',
        leaf='all',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
