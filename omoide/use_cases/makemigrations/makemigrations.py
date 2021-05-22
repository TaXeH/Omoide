# -*- coding: utf-8 -*-

"""Make migrations.
"""
import json
from typing import List, Tuple, Dict, Collection, Optional

import omoide.files.constants
from omoide import core
from omoide.database import constants as db_constants, \
    operations as db_operations, utils as db_utils
from omoide.use_cases import cli
from omoide.use_cases.makemigrations.class_relocation import Relocation
from omoide.use_cases.makemigrations import (
    commands, preprocessing, relocations, saving,
)
from omoide.use_cases.makemigrations.class_sql import SQL


def all_sources(command: cli.MakeMigrationCommand, filesystem: core.Filesystem,
                stdout: core.STDOut):
    """Create migrations for all trunks."""
    stdout.print('Creating migrations for all sources')

    filenames_to_delete = {db_constants.ROOT_DB_FILENAME,
                           db_constants.TRUNK_DB_FILENAME,
                           db_constants.LEAF_DB_FILENAME,
                           omoide.files.constants.MIGRATION_FILENAME,
                           omoide.files.constants.RELOCATION_FILENAME}
    report = drop_files(command.sources_path, filenames_to_delete, filesystem)

    for filename in sorted(filenames_to_delete):
        state = report.get(filename)
        if state is not None:
            stdout.yellow(f'{state["status"]}: {state["path"]}')
        else:
            stdout.red(f'Not found: {filename}')

    uuid_master = core.UUIDMaster()
    renderer = core.Renderer()
    for source in filesystem.list_folders(command.sources_path):
        all_commands, all_relocations = make_migrations_for_single_source(
            sources_path=command.sources_path,
            content_path=command.content_path,
            current_source=source,
            uuid_master=uuid_master,
            renderer=renderer,
            filesystem=filesystem,
            stdout=stdout,
        )

        saving.save_sql_commands(
            source_folder=filesystem.join(command.sources_path, source),
            commands=all_commands,
            filesystem=filesystem,
            stdout=stdout,
        )

        saving.save_relocations(
            source_folder=filesystem.join(command.sources_path, source),
            relocations=all_relocations,
            filesystem=filesystem,
            stdout=stdout,
        )


def one_one_trunk(command: cli.MakeMigrationCommand,
                  filesystem: core.Filesystem,
                  stdout: core.STDOut):
    """Create migrations for single trunk."""
    stdout.print('Creating migrations for single trunk and all leaves')


def one_leaf(command: cli.MakeMigrationCommand, filesystem: core.Filesystem,
             stdout: core.STDOut):
    """Create migrations for single leaf."""
    # stdout.print('Creating migrations for single leaf')
    #
    # leaf_folder = filesystem.join(command.sources_path, command.leaf)
    #
    # if not filesystem.exists(leaf_folder):
    #     raise FileNotFoundError(f'Folder {leaf_folder} does not exist')
    #
    # source_file_path = filesystem.join(command.sources_path,
    #                                    db_constants.SOURCE_FILE)
    #
    # if filesystem.not_exists(source_file_path):
    #     raise FileNotFoundError(f'No source file {source_file_path}')
    #
    # source_raw_text = filesystem.read_file(source_file_path)
    # source_raw_dict = json.loads(source_raw_text)
    # aliases = source_raw_dict.get('aliases', {})
    #
    # paths_to_databases = db_operations.find_all_databases(
    #     sources_folder=leaf_folder,
    #     filesystem=filesystem,
    #     ignore=[(leaf_folder, db_constants.LEAF_DB_FNAME)],
    # )
    # uuid_master = make_global_uuid_master(paths_to_databases, aliases,
    #                                       filesystem, stdout)
    #
    # leaf_db_path = filesystem.join(leaf_folder, db_constants.LEAF_DB_FNAME)
    # database = db_operations.restore_database_from_scratch(
    #     sources_folder=leaf_folder,
    #     filename=db_constants.LEAF_DB_FNAME,
    #     filesystem=filesystem,
    #     stdout=stdout,
    # )


def make_global_uuid_master(paths_to_databases: List[Tuple[str, str]],
                            aliases: Dict[str, str],
                            filesystem: core.Filesystem,
                            stdout: core.STDOut) -> core.UUIDMaster:
    """Create instance of UUIDMater that knows all databases."""
    main_uuid_master = core.UUIDMaster()

    for folder, file in paths_to_databases:
        path = filesystem.join(folder, file)
        if filesystem.not_exists(path):
            stdout.yellow(f'Database does not exist: {path}')
            continue

        database = db_operations.create_database(
            folder=folder,
            filename=file,
            filesystem=filesystem,
            stdout=stdout,
            echo=True,
        )

        uuid_master = db_utils.create_uuid_mater_from_db(database, aliases)
        main_uuid_master += uuid_master

    return main_uuid_master


def drop_files(target_folder: str,
               filenames: Collection[str],
               filesystem: core.Filesystem) -> Dict[str, Dict[str, str]]:
    """Drop all given filenames."""
    filenames = set(filenames)
    report: Dict[str, Dict[str, str]] = {}

    for folder, filename, _, _ in filesystem.iter_ext(target_folder):
        if filename in filenames:
            path = filesystem.join(folder, filename)
            filenames.discard(filename)
            report[filename] = {
                'path': path,
                'status': 'Deleted'
            }
            # FIXME - actually delete the file

    return report


def make_migrations_for_single_source(sources_path: str,
                                      content_path: str,
                                      current_source: str,
                                      uuid_master: core.UUIDMaster,
                                      renderer: core.Renderer,
                                      filesystem: core.Filesystem,
                                      stdout: core.STDOut) \
        -> Optional[Tuple[List[SQL], List[Relocation]]]:
    """Create all migration resources for a single folder."""
    current_source_folder = filesystem.join(sources_path, current_source)
    stdout.print(f'Creating migrations for {current_source_folder}')

    source_file_path = filesystem.join(current_source_folder,
                                       omoide.files.constants.SOURCE_FILENAME)

    if filesystem.not_exists(source_file_path):
        stdout.yellow(f'Source file does not exist: {source_file_path}')
        return None

    source_raw_text = filesystem.read_file(source_file_path)
    source_raw_dict = json.loads(source_raw_text)
    aliases = source_raw_dict.get('aliases', {})
    uuid_master.add_new_aliases(aliases)
    source_text = preprocessing.preprocess_source(source_raw_text, uuid_master)
    source_dict = json.loads(source_text)

    all_objects = preprocessing.instantiate_from_source(
        current_source_folder=current_source_folder,
        content_path=content_path,
        source_dict=source_dict,
        uuid_master=uuid_master,
        filesystem=filesystem,
        renderer=renderer,
    )

    all_commands = commands.instantiate_commands(
        all_objects=all_objects,
    )

    all_relocations = relocations.instantiate_relocations(
        content_path=content_path,
        all_objects=all_objects,
        relocations=all_objects.relocations,
        filesystem=filesystem,
    )

    return all_commands, all_relocations
