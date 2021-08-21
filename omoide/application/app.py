# -*- coding: utf-8 -*-
"""Application.
"""

import flask
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from omoide import commands, constants, utils
from omoide import search_engine
from omoide.application import database, logic
from omoide.application import factories
from omoide.application import search as search_


# pylint: disable=too-many-locals
def create_app(command: commands.RunserverCommand,
               engine: Engine) -> flask.Flask:
    """Create web application instance."""
    app = flask.Flask(import_name='omoide',
                      template_folder=command.templates_folder,
                      static_folder=command.static_folder)
    Session = sessionmaker(bind=engine)  # pylint: disable=invalid-name
    query_builder = search_engine.QueryBuilder(search_engine.Query)

    with database.session_scope(Session) as _session:
        search_index = database.get_index(_session)

    version = f'Version: {constants.VERSION}'
    title = 'Omoide'
    injection = ''  # FIXME

    @app.route('/')
    def index():
        """Entry page."""
        return flask.render_template('index.html')

    @app.context_processor
    def common_names():
        """Populate context with common names."""
        return {
            'title': title,
            'note': version,
            'injection': injection,
            'byte_count_to_text': utils.byte_count_to_text,
            'web_query': '',
        }

    @app.errorhandler(404)
    def page_not_found(exc):
        """Return not found page."""
        # TODO
        assert exc
        context = {
        }
        return flask.render_template('404.html', **context), 404

    @app.route('/navigation', methods=['GET', 'POST'])
    def navigation():
        """Show selection fields for realm/theme."""
        web_query = search_.WebQuery.from_request(flask.request.args)
        current_realm = web_query.get('current_realm', constants.ALL_REALMS)
        current_theme = web_query.get('current_theme', constants.ALL_THEMES)

        if flask.request.method == 'POST':
            web_query = logic.make_navigation_response_post(
                maker=Session,
                web_query=web_query,
                form=flask.request.form,
                current_realm=current_realm,
                abort_callback=flask.abort,
            )
            return flask.redirect(flask.url_for('navigation') + str(web_query))

        context = logic.make_navigation_response_get(
            maker=Session,
            web_query=web_query,
            current_realm=current_realm,
            current_theme=current_theme,
        )

        return flask.render_template('navigation.html', **context)

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        """Main page of the application."""
        web_query = search_.WebQuery.from_request(flask.request.args)

        if flask.request.method == 'POST':
            web_query['q'] = flask.request.form.get('query', '')
            return flask.redirect(flask.url_for('search') + str(web_query))

        context = logic.make_search_response(
            maker=Session,
            web_query=web_query,
            query_builder=query_builder,
            index=search_index,
        )

        return flask.render_template('search.html', **context)

    @app.route('/preview/<uuid>')
    def preview(uuid: str):
        """Show description for a single record."""
        web_query = search_.WebQuery.from_request(flask.request.args)
        context = logic.make_preview_response(
            maker=Session,
            web_query=web_query,
            uuid=uuid,
            abort_callback=flask.abort,
        )
        return flask.render_template('preview.html', **context)

    if command.static:
        factories.add_content(app, Session, command)

    factories.add_tags(app, Session)

    return app
