# -*- coding: utf-8 -*-

"""Run dev server.
"""
import sys

from omoide import commands
from omoide import constants
from omoide import rite
from omoide.database import operations
from omoide.vision.app import create_app


def act(command: commands.RunserverCommand,
        filesystem: rite.Filesystem,
        stdout: rite.STDOut) -> None:
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