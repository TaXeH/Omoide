# -*- coding: utf-8 -*-

"""Create static database.
"""
import sys

from sqlalchemy.orm import sessionmaker

from omoide import commands
from omoide import constants
from omoide import infra
from omoide.migration_engine import persistent
from omoide.database import operations
from omoide.migration_engine.operations.freeze.indexes import build_indexes


def act(command: commands.FreezeCommand,
        filesystem: infra.Filesystem,
        stdout: infra.STDOut) -> None:
    """Create static database."""
    root_db_path = filesystem.join(command.storage_folder,
                                   constants.ROOT_DB_FILE_NAME)

    if filesystem.not_exists(root_db_path):
        stdout.red(f'Source database does not exist: {root_db_path}')
        sys.exit(1)

    root_db = operations.create_database(
        folder=command.storage_folder,
        filename=constants.ROOT_DB_FILE_NAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=False,
    )

    static_filename = constants.STATIC_DB_FILE_NAME.format(
        today=persistent.get_today()
    )
    static_db_path = filesystem.join(command.database_folder, static_filename)

    if filesystem.exists(static_db_path):
        stdout.yellow(f'Deleting old target database: {static_db_path}')
        filesystem.delete_file(static_db_path)

    needs_schema = filesystem.not_exists(static_db_path)
    static_db = operations.create_database(
        folder=command.database_folder,
        filename=static_filename,
        filesystem=filesystem,
        stdout=stdout,
        echo=False,
    )
    if needs_schema:
        operations.create_scheme(static_db, stdout)

    SessionRoot = sessionmaker(bind=root_db)
    session_root = SessionRoot()

    SessionStatic = sessionmaker(bind=static_db)
    session_static = SessionStatic()

    operations.synchronize(session_root, session_static)
    build_indexes(session_static)

    root_db.dispose()
    static_db.dispose()
