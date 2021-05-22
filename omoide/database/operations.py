# -*- coding: utf-8 -*-

"""Basic database operations.
"""
from typing import List, Collection, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from omoide import core
from omoide.database import common, constants


def drop_database(sources_folder: str, filename: str,
                  filesystem: core.Filesystem, stdout: core.STDOut) -> None:
    """Remove database file from folder."""
    path = filesystem.absolute(filesystem.join(sources_folder, filename))

    try:
        filesystem.delete_file(path)
    except FileNotFoundError:
        stdout.yellow(f'Database never existed {path}')
    except OSError:
        stdout.red(f'Could not delete database {path}')
        raise
    else:
        stdout.green(f'Dropped database {path}')


def create_database(folder: str, filename: str,
                    filesystem: core.Filesystem, stdout: core.STDOut,
                    echo: bool) -> Engine:
    """Create database file."""
    path = filesystem.absolute(filesystem.join(folder, filename))
    engine = create_engine(f'sqlite+pysqlite:///{path}',
                           echo=echo,
                           future=True)
    stdout.green(f'Created database {engine}')
    return engine


def create_scheme(database: Engine, stdout: core.STDOut) -> None:
    """Create all required tables."""
    common.metadata.create_all(bind=database)
    stdout.green('Created all tables')


def restore_database_from_scratch(sources_folder: str,
                                  filename: str,
                                  filesystem: core.Filesystem,
                                  stdout: core.STDOut,
                                  echo: bool = True) -> Engine:
    """Drop existing leaf database and create a new one.
    """
    drop_database(
        sources_folder=sources_folder,
        filename=filename,
        filesystem=filesystem,
        stdout=stdout,
    )

    database = create_database(
        folder=sources_folder,
        filename=filename,
        filesystem=filesystem,
        stdout=stdout,
        echo=echo,
    )

    create_scheme(
        database=database,
        stdout=stdout,
    )

    return database


def find_all_databases(sources_folder: str,
                       filesystem: core.Filesystem,
                       ignore: Collection[Tuple[str, str]]
                       ) -> List[Tuple[str, str]]:
    """Find paths to all databases, root, trunk and leaves.

    Folder structure is supposed to look like:
    root_folder
        ├── root.db
        ├── source_1
        │   ├── migration_1
        │   │   └── migration.db
        │   ├── migration_2
        │   │   └── migration.db
        │   └── trunk.db
        └── source_2
            └── migration_3
                └── migration.db
    """
    ignore = set(ignore)
    databases = []

    root_file = filesystem.join(sources_folder, constants.ROOT_DB_FILENAME)
    if filesystem.exists(root_file):
        databases.append((sources_folder, constants.ROOT_DB_FILENAME))

    for folder in filesystem.list_folders(sources_folder):
        trunk_path = filesystem.join(sources_folder, folder)
        trunk_file = filesystem.join(trunk_path, constants.TRUNK_DB_FILENAME)

        if filesystem.exists(trunk_file):
            databases.append((trunk_path, constants.TRUNK_DB_FILENAME))

        for sub_folder in filesystem.list_folders(trunk_path):
            leaf_path = filesystem.join(trunk_path, sub_folder)
            leaf_file = filesystem.join(leaf_path, constants.LEAF_DB_FILENAME)

            if filesystem.exists(leaf_file):
                databases.append((leaf_path, constants.LEAF_DB_FILENAME))

    return [x for x in databases if x not in ignore]
