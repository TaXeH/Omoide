# -*- coding: utf-8 -*-

"""Basic database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from omoide import infra
from omoide.database import common, models

__all__ = [
    'drop_database',
    'create_database',
    'create_scheme',
    'restore_database_from_scratch',
    'synchronize',
]


def drop_database(sources_folder: str, filename: str,
                  filesystem: infra.Filesystem) -> bool:
    """Remove database file from folder."""
    path = filesystem.absolute(filesystem.join(sources_folder, filename))
    dropped = False

    try:
        filesystem.delete_file(path)
    except FileNotFoundError:
        pass
    else:
        dropped = True

    return dropped


def create_database(folder: str, filename: str,
                    filesystem: infra.Filesystem,
                    echo: bool) -> Engine:
    """Create database file."""
    path = filesystem.absolute(filesystem.join(folder, filename))
    engine = create_engine(f'sqlite+pysqlite:///{path}',
                           echo=echo,
                           future=True)
    return engine


def create_read_only_database(folder: str, filename: str,
                              filesystem: infra.Filesystem,
                              echo: bool) -> Engine:
    """Create database file."""
    path = filesystem.absolute(filesystem.join(folder, filename))
    engine = create_engine(f'sqlite+pysqlite:///{path}?uri=true',
                           connect_args={'check_same_thread': False},
                           echo=echo,
                           future=True)
    return engine


def create_scheme(database: Engine) -> None:
    """Create all required tables."""
    common.metadata.create_all(bind=database)


def restore_database_from_scratch(folder: str,
                                  filename: str,
                                  filesystem: infra.Filesystem,
                                  echo: bool = True) -> Engine:
    """Drop existing leaf database and create a new one.
    """
    drop_database(sources_folder=folder,
                  filename=filename,
                  filesystem=filesystem)

    database = create_database(folder=folder,
                               filename=filename,
                               filesystem=filesystem,
                               echo=echo)

    create_scheme(database)

    return database


def synchronize(session_from: Session, session_to: Session) -> None:
    """Synchronize objects from one database to another."""
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
    sync_model(session_from, session_to, models.PermissionGroup)

    sync_model(session_from, session_to, models.Meta)
    sync_model(session_from, session_to, models.TagMeta)
    sync_model(session_from, session_to, models.PermissionMeta)

    sync_model(session_from, session_to, models.User)
    sync_model(session_from, session_to, models.PermissionUser)


def sync_model(session_from: Session, session_to: Session, model) -> None:
    """Synchronize single model from one database to another."""
    for each in session_from.query(model).all():
        each = session_to.merge(each)
        session_to.add(each)
    session_to.commit()


def select_newest_filename(folder: str, filesystem: infra.Filesystem) -> str:
    """From all databases select the newest one."""
    files = filesystem.list_files(folder)
    files.sort()
    return files[-1]
