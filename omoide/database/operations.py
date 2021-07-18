# -*- coding: utf-8 -*-

"""Basic database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from omoide import rite
from omoide.database import common, models

__all__ = [
    'drop_database',
    'create_database',
    'create_scheme',
    'restore_database_from_scratch',
    'synchronize',
]


def drop_database(sources_folder: str, filename: str,
                  filesystem: rite.Filesystem, stdout: rite.STDOut) -> None:
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
                    filesystem: rite.Filesystem, stdout: rite.STDOut,
                    echo: bool) -> Engine:
    """Create database file."""
    path = filesystem.absolute(filesystem.join(folder, filename))
    engine = create_engine(f'sqlite+pysqlite:///{path}',
                           echo=echo,
                           future=True)
    stdout.green(f'Created database {engine}')
    return engine


def create_read_only_database(folder: str, filename: str,
                              filesystem: rite.Filesystem,
                              stdout: rite.STDOut,
                              echo: bool) -> Engine:
    """Create database file."""
    path = filesystem.absolute(filesystem.join(folder, filename))
    engine = create_engine(f'sqlite+pysqlite:///{path}?uri=true',
                           connect_args={'check_same_thread': False},
                           echo=echo,
                           future=True)
    stdout.green(f'Created database {engine}')
    return engine


def create_scheme(database: Engine, stdout: rite.STDOut) -> None:
    """Create all required tables."""
    common.metadata.create_all(bind=database)
    stdout.green('Created all tables')


def restore_database_from_scratch(folder: str,
                                  filename: str,
                                  filesystem: rite.Filesystem,
                                  stdout: rite.STDOut,
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


def synchronize(session_from: Session, session_to: Session) -> None:
    """"""
    sync_model(session_from, session_to, models.Realm)
    sync_model(session_from, session_to, models.TagRealm)
    sync_model(session_from, session_to, models.PermissionRealm)
    sync_model(session_from, session_to, models.Theme)
    sync_model(session_from, session_to, models.TagTheme)
    sync_model(session_from, session_to, models.PermissionTheme)
    sync_model(session_from, session_to, models.Synonym)
    sync_model(session_from, session_to, models.SynonymValue)
    sync_model(session_from, session_to, models.ImplicitTag)
    sync_model(session_from, session_to, models.ImplicitTagValue)
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
