# -*- coding: utf-8 -*-

"""Basic database operations.
"""
from typing import List, Collection, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import omoide.constants
from omoide import core
from omoide.database import common, models

__all__ = [
    'drop_database',
    'create_database',
    'create_scheme',
    'restore_database_from_scratch',
]


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


def restore_database_from_scratch(folder: str,
                                  filename: str,
                                  filesystem: core.Filesystem,
                                  stdout: core.STDOut,
                                  echo: bool = True) -> Engine:
    """Drop existing leaf database and create a new one.
    """
    drop_database(
        sources_folder=folder,
        filename=filename,
        filesystem=filesystem,
        stdout=stdout,
    )

    database = create_database(
        folder=folder,
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
    """Find paths to all databases, root, branch and leaves.

    Folder structure is supposed to look like:
    root_folder
        ├── root.db
        ├── source_1
        │   ├── migration_1
        │   │   └── migration.db
        │   ├── migration_2
        │   │   └── migration.db
        │   └── branch.db
        └── source_2
            └── migration_3
                └── migration.db
    """
    ignore = set(ignore)
    databases = []

    root_file = filesystem.join(sources_folder,
                                omoide.constants.ROOT_DB_FILENAME)
    if filesystem.exists(root_file):
        databases.append((sources_folder, omoide.constants.ROOT_DB_FILENAME))

    for folder in filesystem.list_folders(sources_folder):
        branch_path = filesystem.join(sources_folder, folder)
        branch_file = filesystem.join(branch_path,
                                      omoide.constants.BRANCH_DB_FILENAME)

        if filesystem.exists(branch_file):
            databases.append(
                (branch_path, omoide.constants.BRANCH_DB_FILENAME))

        for sub_folder in filesystem.list_folders(branch_path):
            leaf_path = filesystem.join(branch_path, sub_folder)
            leaf_file = filesystem.join(leaf_path,
                                        omoide.constants.LEAF_DB_FILENAME)

            if filesystem.exists(leaf_file):
                databases.append((leaf_path,
                                  omoide.constants.LEAF_DB_FILENAME))

    return [x for x in databases if x not in ignore]


def synchronize(session_from: Session, session_to: Session) -> None:
    """"""
    sync_model(session_from, session_to, models.Realm)
    sync_model(session_from, session_to, models.TagRealm)
    sync_model(session_from, session_to, models.PermissionRealm)
    sync_model(session_from, session_to, models.Theme)
    sync_model(session_from, session_to, models.TagTheme)
    sync_model(session_from, session_to, models.PermissionTheme)
    sync_model(session_from, session_to, models.Synonym)
    sync_model(session_from, session_to, models.ImplicitTag)
    sync_model(session_from, session_to, models.Group)
    sync_model(session_from, session_to, models.TagGroup)
    sync_model(session_from, session_to, models.Meta)
    sync_model(session_from, session_to, models.TagMeta)
    sync_model(session_from, session_to, models.User)
    sync_model(session_from, session_to, models.PermissionUser)


def sync_model(session_from: Session, session_to: Session, model) -> None:
    for each in session_from.query(model).all():
        each = session_to.merge(each)
        session_to.add(each)
    session_to.commit()
