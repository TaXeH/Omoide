# -*- coding: utf-8 -*-
"""Constructors of the app.
"""

import flask
from flask import request
from sqlalchemy.orm import sessionmaker

from omoide import constants, commands
from omoide.application import search as search_, database


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


def add_tags(app, maker: sessionmaker) -> None:
    """Add tags tab."""

    @app.route('/tags')
    def tags():
        """Show available tags."""
        web_query = search_.WebQuery.from_request(request.args)
        user_query = web_query.get('q')

        with database.session_scope(maker) as session:
            current_realm = web_query.get('current_realm',
                                          constants.ALL_REALMS)
            current_theme = web_query.get('current_theme',
                                          constants.ALL_THEMES)
            stats = database.get_stats(session, current_realm, current_theme)

        context = {
            'web_query': web_query,
            'user_query': user_query,
            'stats': stats,
            'tags_by_frequency': stats.get('Tags by frequency', {}),
            'tags_by_alphabet': stats.get('Tags by alphabet', {}),
        }
        return flask.render_template('tags.html', **context)
