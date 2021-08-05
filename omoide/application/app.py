# -*- coding: utf-8 -*-
"""Application.
"""
import time

import flask
from flask import request, abort
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from omoide import commands
from omoide import constants
from omoide import utils
from omoide.application import appearance
from omoide.application import database
from omoide.application import navigation as nav
from omoide.application import search as search_helpers
from omoide.application.search import search_routine
from omoide.application.search.class_paginator import Paginator


def create_app(command: commands.RunserverCommand,
               engine: Engine) -> flask.Flask:
    """Create web application instance."""
    app = flask.Flask(
        import_name='omoide',
        template_folder=command.template_folder,
        static_folder=command.static_folder,
    )
    Session = sessionmaker(bind=engine)
    query_builder = search_helpers.QueryBuilder(search_helpers.Query)

    _session = Session()
    search_index = database.get_index(_session)
    _session.close()

    @app.context_processor
    def common_names():
        """Populate context with common names."""
        return {
            'title': '',  # FIXME
            'note': f'Version: {constants.VERSION}',
            'injection': '',  # FIXME
            'byte_count_to_text': utils.byte_count_to_text,
        }

    @app.route('/content/<path:filename>')
    def serve_content(filename: str):
        """Serve files from main storage.

        Contents of the main storage are served through this function.
        It's not about static css or js files. Not supposed to be used
        in production.
        """
        return flask.send_from_directory(command.content_folder,
                                         filename, conditional=True)

    @app.route('/')
    def index():
        """Entry page."""
        return flask.render_template('index.html')

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        """Main page of the application."""
        web_query = search_helpers.WebQuery.from_request(request.args)

        if request.method == 'POST':
            web_query['q'] = request.form.get('query', '')
            return flask.redirect(flask.url_for('search') + str(web_query))

        start = time.perf_counter()
        # session = Session()
        user_query = web_query.get('q')
        current_page = int(web_query.get('page', '1'))

        query = query_builder.from_query(user_query)

        # realm_route = web_query.get('realm_route', constants.ALL_REALMS)
        # if realm_route and realm_route != constants.ALL_REALMS:
        #     realm_uuid = database.get_realm_uuid(session,
        #                                          realm_route) or abort(404)
        #     query.and_.add(realm_uuid)
        #
        # theme_route = web_query.get('theme_route', constants.ALL_THEMES)
        # if theme_route and theme_route != constants.ALL_THEMES:
        #     theme_uuid = database.get_theme_uuid(session,
        #                                          theme_route) or abort(404)
        #     query.and_.add(theme_uuid)
        #
        # group_route = web_query.get('group_route', constants.ALL_GROUPS)
        # if group_route and group_route != constants.ALL_GROUPS:
        #     group_uuid = database.get_group_uuid(session,
        #                                          group_route) or abort(404)
        #     query.and_.add(group_uuid)

        if query:
            uuids = search_routine.find_records(query, search_index, 50)
        else:
            uuids = search_routine.random_records(search_index, 50)

        paginator = Paginator(
            sequence=uuids,
            current_page=current_page,
            items_per_page=50,  # FIXME
        )

        duration = time.perf_counter() - start
        note = appearance.get_note_on_search(len(paginator), duration)

        context = {
            'title': 'test',
            'paginator': paginator,
            'user_query': user_query,
            'web_query': web_query,
            'note': note,
            'placeholder': '',
            # 'placeholder': utils_browser.get_placeholder(current_theme),
        }
        return flask.render_template('search.html', **context)

    @app.route('/preview/<uuid>')
    def preview(uuid: str):
        """Show description for a single record."""
        session = Session()
        meta = database.get_meta(session, uuid) or abort(404)
        web_query = search_helpers.WebQuery.from_request(request.args)
        tags = {
            *[x.value for x in meta.group.theme.realm.tags],
            *[x.value for x in meta.group.theme.tags],
            *[x.value for x in meta.group.tags],
            *[x.value for x in meta.tags],
        }
        context = {
            'meta': meta,
            'web_query': web_query,
            'tags': sorted(tags),
        }
        return flask.render_template('preview.html', **context)

    @app.route('/navigation')
    def navigation():
        """Show selection fields for realm/theme."""
        web_query = search_helpers.WebQuery.from_request(request.args)

        if request.method == 'POST':
            web_query['q'] = request.form.get('query', '')
            return flask.redirect(flask.url_for('navigation') + str(web_query))

        current_realm = web_query.get('current_realm', constants.ALL_REALMS)
        current_theme = web_query.get('current_theme', constants.ALL_THEMES)

        session = Session()
        raw_graph = database.get_graph(session)
        # graph = appearance.format_graph(raw_graph,
        #                                 current_realm, current_theme)
        stats = database.get_stats(session, current_realm, current_theme)

        dimensions = nav.calculate_table_dimensions(raw_graph)
        initials = []
        coordinates = {}
        table = nav.generate_empty_table(*dimensions)
        nav.populate_table(table, raw_graph, initials, coordinates)
        nav.continue_lines(table, initials)

        context = {
            'web_query': web_query,
            # 'graph': graph,
            # 'stats': stats,
            'table': table,
            # 'tags_by_frequency': stats['Tags by frequency'],
            # 'tags_by_alphabet': stats['Tags by alphabet'],
        }
        return flask.render_template('navigation.html', **context)

    @app.errorhandler(404)
    def page_not_found(exc):
        """Return not found page."""
        context = {
            # 'directory': constants.ALL_THEMES,
        }
        return flask.render_template('404.html', **context), 404

    return app
