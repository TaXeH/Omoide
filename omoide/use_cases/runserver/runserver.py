# -*- coding: utf-8 -*-

"""Run dev server.
"""
import sys

from omoide import constants, use_cases
from omoide import core
from omoide.database import operations
from omoide.use_cases import commands
from omoide.vision.app import create_app


def act(command: use_cases.RunserverCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> None:
    """Run dev server."""
    static_db_path = filesystem.join(command.content_folder,
                                     constants.STATIC_DB_FILE_NAME)

    if filesystem.not_exists(static_db_path):
        stdout.red(f'Source database does not exist: {static_db_path}')
        sys.exit(1)

    engine = operations.create_read_only_database(
        folder=command.content_folder,
        filename=constants.STATIC_DB_FILE_NAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )

    app = create_app(command, engine)
    app.run(host=command.host, port=command.port, debug=True)


if __name__ == '__main__':
    cmd = commands.RunserverCommand(
        host='127.0.0.1',
        port=5000,
        sources_folder='',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
        storage_folder='',
        branch='',
        leaf='',
        template_folder='D:\\PycharmProjects\\'
                        'Omoide\\omoide\\vision\\templates',
        static_folder='D:\\PycharmProjects\\'
                      'Omoide\\omoide\\vision\\static',
    )
    fs = core.Filesystem()
    st = core.STDOut()
    act(cmd, filesystem=fs, stdout=st)
