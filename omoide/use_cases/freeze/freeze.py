# -*- coding: utf-8 -*-

"""Create static database.
"""
import sys

from sqlalchemy.orm import sessionmaker

from omoide import constants
from omoide import core
from omoide.database import operations
from omoide.use_cases import commands
from omoide.use_cases.freeze.indexes import build_indexes


def act(command: commands.FreezeCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> None:
    """Create static database."""
    root_db_path = filesystem.join(command.sources_folder,
                                   constants.ROOT_DB_FILENAME)
    static_db_path = filesystem.join(command.content_folder,
                                     constants.STATIC_DB_FILENAME)

    if filesystem.not_exists(root_db_path):
        stdout.red(f'Source database does not exist: {root_db_path}')
        sys.exit(1)

    # if filesystem.exists(static_db_path):
    #     stdout.yellow(f'Deleting old target database: {static_db_path}')
    #     filesystem.delete_file(static_db_path)

    root = operations.create_database(
        folder=command.sources_folder,
        filename=constants.ROOT_DB_FILENAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )

    needs_schema = filesystem.not_exists(static_db_path)
    static = operations.create_database(
        folder=command.content_folder,
        filename=constants.STATIC_DB_FILENAME,
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


if __name__ == '__main__':
    cmd = commands.FreezeCommand(
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    fs = core.Filesystem()
    st = core.STDOut()
    act(cmd, filesystem=fs, stdout=st)
