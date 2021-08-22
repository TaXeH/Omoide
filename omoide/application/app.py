# -*- coding: utf-8 -*-
"""Production application launcher.
"""

from omoide import commands, constants, infra
from omoide.application import app_factory
from omoide.database import operations

filesystem = infra.Filesystem()
root = filesystem.absolute('.')
command = commands.RunserverCommand(
    reload=False,
    static=False,
    database_folder=filesystem.join(root, constants.DATABASE_FOLDER_NAME),
    content_folder=filesystem.join(root, constants.CONTENT_FOLDER_NAME),
    templates_folder=filesystem.join(root, constants.TEMPLATES_FOLDER_NAME),
)

engine = operations.create_read_only_database(
    folder=filesystem.join(root, constants.DATABASE_FOLDER_NAME),
    filename=constants.STATIC_DB_FILE_NAME,
    filesystem=filesystem,
    echo=False,
)

app = app_factory.create_app(command, engine)
