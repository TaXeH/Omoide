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
from omoide.migration_engine.operations.freeze import indexes
from omoide.migration_engine.operations.freeze import helpers


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
        echo=False,
    )

    db_filename = constants.STATIC_DB_FILE_NAME.format(
        today=persistent.get_today()
    )
    db_path = filesystem.join(command.database_folder, db_filename)

    if filesystem.exists(db_path):
        stdout.yellow(f'Deleting old target database: {db_path}')
        filesystem.delete_file(db_path)

    needs_schema = filesystem.not_exists(db_path)
    database = operations.create_database(
        folder=command.database_folder,
        filename=db_filename,
        filesystem=filesystem,
        echo=False,
    )
    if needs_schema:
        operations.create_scheme(database)

    SessionRoot = sessionmaker(bind=root_db)
    session_root = SessionRoot()

    SessionDb = sessionmaker(bind=database)
    session_db = SessionDb()

    operations.synchronize(session_root, session_db)
    indexes.build_indexes(session_db, stdout)
    helpers.build_helpers(session_db, stdout)

    root_db.dispose()
    database.dispose()
