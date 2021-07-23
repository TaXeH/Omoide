# -*- coding: utf-8 -*-

"""Run dev server.
"""
import sys

from omoide import commands
from omoide import infra
from omoide.application.app import create_app
from omoide.database import operations


def act(command: commands.RunserverCommand,
        filesystem: infra.Filesystem,
        stdout: infra.STDOut) -> None:
    """Run dev server."""
    filename = operations.select_newest_filename(command.database_folder,
                                                 filesystem)
    static_db_path = filesystem.join(command.database_folder, filename)

    if filesystem.not_exists(static_db_path):
        stdout.red(f'Source database does not exist: {static_db_path}')
        sys.exit(1)

    engine = operations.create_read_only_database(
        folder=command.database_folder,
        filename=filename,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )

    app = create_app(command, engine)
    app.run(host=command.host, port=command.port, debug=True)
