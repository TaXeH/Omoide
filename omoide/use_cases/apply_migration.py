# -*- coding: utf-8 -*-

"""Apply migration.
"""
from sqlalchemy import text

import omoide.files.constants
from omoide import core
from omoide.database import constants
from omoide.database import operations

__all__ = [
    'apply_all_migrations_in_source_folder',
    'apply_migration_in_one_folder',
]


def apply_all_migrations_in_source_folder(source_folder: str,
                                          filesystem: core.Filesystem,
                                          stdout: core.STDOut) -> None:
    """Handle all migrations in all subfolders.
    """
    for subfolder_name in filesystem.list_folders(source_folder):
        source_subfolder = filesystem.join(source_folder, subfolder_name)

        apply_migration_in_one_folder(source_folder=source_subfolder,
                                      filesystem=filesystem,
                                      stdout=stdout)


def apply_migration_in_one_folder(source_folder: str,
                                  filesystem: core.Filesystem,
                                  stdout: core.STDOut) -> None:
    """Handle all migrations in all subfolders.
    """
    migration_file_path = filesystem.join(source_folder,
                                          omoide.files.constants.MIGRATION_FILENAME)

    if filesystem.not_exists(migration_file_path):
        stdout.yellow(f'Nothing to migrate in {source_folder}')
        return

    database = operations.restore_database_from_scratch(
        sources_folder=source_folder,
        filename=constants.LEAF_DB_FILENAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=False,
    )

    migration_file = filesystem.read_file(migration_file_path)

    with database.connect() as connection:
        for line in migration_file.split(';\n'):
            connection.execute(text(line))
        connection.commit()

    stdout.green(f'Applied migration {migration_file_path} to the {database}')
