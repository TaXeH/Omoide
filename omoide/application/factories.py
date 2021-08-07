# -*- coding: utf-8 -*-
"""Constructors of the app.
"""
import time

import flask
from flask import request, abort
from sqlalchemy.orm import sessionmaker

from omoide import constants, utils, commands
from omoide.application import navigation as navigation_, appearance
from omoide.application import search as search_, database
from omoide.application.search import search_routine
from omoide.application.search.class_paginator import Paginator


def add_basics(app, Session: sessionmaker) -> None:
    """Add basic views."""
    assert Session  # FIXME
    version = f'Version: {constants.VERSION}'

    @app.route('/')
    def index():
        """Entry page."""
        return flask.render_template('index.html')

    @app.context_processor
    def common_names():
        """Populate context with common names."""
        return {
            'title': '',  # FIXME
            'note': version,
            'injection': '',  # FIXME
            'byte_count_to_text': utils.byte_count_to_text,
            'web_query': '',
        }

    @app.errorhandler(404)
    def page_not_found(exc):
        """Return not found page."""
        # TODO
        assert exc
        context = {
            # 'directory': constants.ALL_THEMES,
        }
        return flask.render_template('404.html', **context), 404


def add_navigation(app, Session: sessionmaker) -> None:
    """Add navigation tab."""

    @app.route('/navigation', methods=['GET', 'POST'])
    def navigation():
        """Show selection fields for realm/theme."""
        web_query = search_.WebQuery.from_request(request.args)
        user_query = web_query.get('q')
        current_realm = web_query.get('current_realm', constants.ALL_REALMS)
        current_theme = web_query.get('current_theme', constants.ALL_THEMES)

        if request.method == 'POST':
            with database.session_scope(Session) as session:
                if 'current_theme' in request.form:
                    theme_uuid = request.form['current_theme']
                    realm_uuid = database.get_realm_uuid_for_theme_uuid(
                        session=session,
                        theme_uuid=theme_uuid,
                        previous_realm=current_realm,
                    )
                    if realm_uuid is None:
                        abort(404)

                    web_query['current_realm'] = realm_uuid
                    web_query['current_theme'] = theme_uuid

                elif 'current_realm' in request.form:
                    web_query['current_realm'] = request.form['current_realm']

            return flask.redirect(flask.url_for('navigation') + str(web_query))

        with database.session_scope(Session) as session:
            graph = database.get_graph(session)

        table, highlight = navigation_.get_table_with_highlight(
            graph=graph,
            current_realm=current_realm,
            current_theme=current_theme,
        )

        context = {
            'web_query': web_query,
            'user_query': user_query,
            'table': table,
            'highlight': highlight,
            'all_realms_active': current_realm == constants.ALL_REALMS,
            'all_themes_active': current_theme == constants.ALL_THEMES,
        }
        return flask.render_template('navigation.html', **context)


def add_content(app, Session: sessionmaker,
                command: commands.RunserverCommand) -> None:
    """Add static files serving."""
    assert Session  # FIXME

    @app.route('/content/<path:filename>')
    def serve_content(filename: str):
        """Serve files from main storage.

        Contents of the main storage are served through this function.
        It's not about static css or js files. Not supposed to be used
        in production.
        """
        return flask.send_from_directory(command.content_folder,
                                         filename, conditional=True)


def add_tags(app, Session: sessionmaker) -> None:
    """Add tags tab."""

    @app.route('/tags')
    def tags():
        """Show available tags."""
        web_query = search_.WebQuery.from_request(request.args)
        user_query = web_query.get('q')

        with database.session_scope(Session) as session:
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


def add_preview(app, Session: sessionmaker) -> None:
    """Add preview tab."""

    @app.route('/preview/<uuid>')
    def preview(uuid: str):
        """Show description for a single record."""
        with database.session_scope(Session) as session:
            meta = database.get_meta(session, uuid) or abort(404)

        web_query = search_.WebQuery.from_request(request.args)
        all_tags = {
            *[x.value for x in meta.group.theme.realm.tags],
            *[x.value for x in meta.group.theme.tags],
            *[x.value for x in meta.group.tags],
            *[x.value for x in meta.tags],
        }
        context = {
            'meta': meta,
            'web_query': web_query,
            'tags': sorted(all_tags),
        }
        return flask.render_template('preview.html', **context)


def add_search(app, Session: sessionmaker,
               query_builder: search_.QueryBuilder,
               search_index: search_.Index) -> None:
    """Add search tab."""

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        """Main page of the application."""
        web_query = search_.WebQuery.from_request(request.args)
        current_realm = web_query.get('current_realm', constants.ALL_REALMS)
        current_theme = web_query.get('current_theme', constants.ALL_THEMES)

        if request.method == 'POST':
            web_query['q'] = request.form.get('query', '')
            return flask.redirect(flask.url_for('search') + str(web_query))

        start = time.perf_counter()
        session = Session()
        assert session

        user_query = web_query.get('q')
        current_page = int(web_query.get('page', '1'))

        query = query_builder.from_query(user_query)

        if current_realm != constants.ALL_REALMS:
            query.and_.add(current_realm)

        if current_theme != constants.ALL_THEMES:
            query.and_.add(current_theme)

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
            'placeholder': appearance.get_placeholder(current_realm,
                                                      current_theme),
        }
        return flask.render_template('search.html', **context)
