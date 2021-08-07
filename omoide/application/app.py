# -*- coding: utf-8 -*-
"""Application.
"""

import flask
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from omoide import commands
from omoide.application import database
from omoide.application import factories
from omoide.application import search as search_helpers


def create_app(command: commands.RunserverCommand,
               engine: Engine) -> flask.Flask:
    """Create web application instance."""
    app = flask.Flask(
        import_name='omoide',
        template_folder=command.template_folder,
        static_folder=command.static_folder,
    )
    Session = sessionmaker(bind=engine)  # pylint: disable=invalid-name
    query_builder = search_helpers.QueryBuilder(search_helpers.Query)

    with database.session_scope(Session) as _session:
        search_index = database.get_index(_session)

    factories.add_basics(app, Session)
    factories.add_navigation(app, Session)
    factories.add_content(app, Session, command)  # TODO - only for dev mode
    factories.add_tags(app, Session)
    factories.add_preview(app, Session)
    factories.add_search(app, Session, query_builder, search_index)

    return app
