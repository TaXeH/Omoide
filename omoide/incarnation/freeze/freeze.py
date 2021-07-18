# -*- coding: utf-8 -*-

"""Create static database.
"""
import sys

from sqlalchemy.orm import sessionmaker

from omoide import commands
from omoide import constants
from omoide import rite
from omoide.database import operations
from omoide.incarnation.freeze.indexes import build_indexes


def act(command: commands.FreezeCommand,
        filesystem: rite.Filesystem,
        stdout: rite.STDOut) -> None:
    """Create static database."""
    root_db_path = filesystem.join(command.storage_folder,
                                   constants.ROOT_DB_FILE_NAME)
    static_db_path = filesystem.join(command.content_folder,
                                     constants.STATIC_DB_FILE_NAME)

    if filesystem.not_exists(root_db_path):
        stdout.red(f'Source database does not exist: {root_db_path}')
        sys.exit(1)

    if filesystem.exists(static_db_path):
        stdout.yellow(f'Deleting old target database: {static_db_path}')
        filesystem.delete_file(static_db_path)

    root = operations.create_database(
        folder=command.storage_folder,
        filename=constants.ROOT_DB_FILE_NAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )

    needs_schema = filesystem.not_exists(static_db_path)
    static = operations.create_database(
        folder=command.content_folder,
        filename=constants.STATIC_DB_FILE_NAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )
    if needs_schema:
        operations.create_scheme(static, stdout)

    SessionRoot = sessionmaker(bind=root)
    session_root = SessionRoot()

    SessionStatic = sessionmaker(bind=static)
    session_static = SessionStatic()

    operations.synchronize(session_root, session_static)
    build_indexes(session_static)
