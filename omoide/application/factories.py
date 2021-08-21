# -*- coding: utf-8 -*-
"""Constructors of the app.
"""

import flask
from sqlalchemy.orm import sessionmaker

from omoide import commands


def add_content(app, maker: sessionmaker,
                command: commands.RunserverCommand) -> None:
    """Add static files serving."""
    assert maker  # FIXME

    @app.route('/content/<path:filename>')
    def serve_content(filename: str):
        """Serve files from main storage.

        Contents of the main storage are served through this function.
        It's not about static css or js files. Not supposed to be used
        in production.
        """
        return flask.send_from_directory(command.content_folder,
                                         filename, conditional=True)
