# -*- coding: utf-8 -*-

"""Make migrations.
"""
from typing import Any, Dict, Tuple, List

import omoide.files.constants
from omoide import core
from omoide.files.operations import drop_files
from omoide.use_cases import commands
from omoide.use_cases.make_migrations import saving
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
    drop_files(command.sources_folder, filenames_to_delete, filesystem, stdout)

    uuid_master = core.UUIDMaster()
    renderer = core.Renderer()

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
                leaf_folder=leaf_folder,
                content_folder=command.content_folder,
                uuid_master=uuid_master,
                renderer=renderer,
                filesystem=filesystem,
                stdout=stdout,
            )
            total_new_migrations += 1

    return total_new_migrations


def make_migrations_for_single_leaf(leaf_folder: str,
                                    content_folder: str,
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

    update_file = make_update_file(leaf_folder, uuid_master,
                                   filesystem, stdout)

    update_file_path = filesystem.join(leaf_folder,
                                       omoide.files.constants.UPDATE_FILENAME)

    filesystem.write_json(update_file_path, update_file)
    stdout.yellow(f'Created update file: {update_file_path}')

    migrations, relocations = make_migrations_from_update_file(update_file,
                                                               content_folder,
                                                               renderer,
                                                               filesystem,
                                                               stdout)
    migrations_path = saving.save_migrations(
        leaf_folder=leaf_folder,
        migrations=migrations,
        filesystem=filesystem,
    )
    stdout.yellow(f'Created migrations file: {migrations_path}')

    relocations_path = saving.save_relocations(
        leaf_folder=leaf_folder,
        relocations=relocations,
        filesystem=filesystem,
    )
    stdout.yellow(f'Created relocations path: {relocations_path}')


def make_update_file(leaf_folder: str,
                     uuid_master: core.UUIDMaster,
                     filesystem: core.Filesystem,
                     stdout: core.STDOut) -> Dict[str, Any]:
    """Combine all updates in big JSON file."""
    return {}


def make_migrations_from_update_file(update: Dict[str, Any],
                                     content_folder: str,
                                     renderer: core.Renderer,
                                     filesystem: core.Filesystem,
                                     stdout: core.STDOut) \
        -> Tuple[List[SQL], List[Relocation]]:
    """Create SQL migrations and relocations."""
    return [], []


#     source_raw_text = filesystem.read_file(source_file_path)
#     source_raw_dict = json.loads(source_raw_text)
#     aliases = source_raw_dict.get('aliases', {})
#     uuid_master.add_new_aliases(aliases)
#     source_text = preprocessing.preprocess_source(source_raw_text, uuid_master)
#     source_dict = json.loads(source_text)
#
#     all_objects = preprocessing.instantiate_from_source(
#         current_source_folder=current_source_folder,
#         content_path=content_path,
#         source_dict=source_dict,
#         uuid_master=uuid_master,
#         filesystem=filesystem,
#         renderer=renderer,
#     )
#
#     all_commands = commands.instantiate_commands(
#         all_objects=all_objects,
#     )
#
#     all_relocations = relocations.instantiate_relocations(
#         content_path=content_path,
#         all_objects=all_objects,
#         relocations=all_objects.relocations,
#         filesystem=filesystem,
#     )
#
#     return all_commands, all_relocations

# for source in filesystem.list_folders(command.sources_path):
#     all_commands, all_relocations = make_migrations_for_single_source(
#         sources_path=command.sources_path,
#         content_path=command.content_path,
#         current_source=source,
#         uuid_master=uuid_master,
#         renderer=renderer,
#         filesystem=filesystem,
#         stdout=stdout,
#     )


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
