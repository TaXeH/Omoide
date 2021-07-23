import time

import flask
from flask import request, abort
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from omoide import constants
from omoide import commands
from omoide.utils import byte_count_to_text
from omoide.application import database
from omoide.application import search
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
    query_builder = search.QueryBuilder(target_type=search.Query)

    _session = Session()
    index_thumbnails = database.get_index_thumbnails(_session)

    @app.context_processor
    def common_names():
        """Populate context with common names."""
        return {
            # 'title': config['title'],
            'note': '',
            # 'injection': config['injection'],
            # 'rewrite_query_for_paging': utils_browser.rewrite_query_for_paging,
            'byte_count_to_text': byte_count_to_text,
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
    def index_entry():
        """Entry page."""
        return flask.redirect(
            flask.url_for(
                'index',
                realm_route=constants.ALL_REALMS,
                theme_route=constants.ALL_THEMES,
                group_route=constants.ALL_GROUPS,
            )
        )

    @app.route('/<realm_route>/<theme_route>/<group_route>/',
               methods=['GET', 'POST'])
    def index(realm_route: str, theme_route: str, group_route: str):
        """Main page of the script."""
        session = Session()
        # if request.method == 'POST':
        #     return utils_browser.add_query_to_path(request, directory)

        start = time.perf_counter()
        query_text = request.args.get('q', '')
        current_page = int(request.args.get('page', 1))

        realm_uuid = database.get_realm_uuid(session,
                                             realm_route) or abort(404)
        theme_uuid = database.get_theme_uuid(session,
                                             theme_route) or abort(404)
        group_uuid = database.get_group_uuid(session,
                                             group_route) or abort(404)

        query = query_builder.from_query(realm_uuid, theme_uuid,
                                         group_uuid, query_text)

        if current_realm and current_realm != constants.ALL_REALMS:
            sets['and_'].add(current_realm)

        if current_theme and current_theme != constants.ALL_THEMES:
            sets['and_'].add(current_theme)

        if current_group and current_group != constants.ALL_GROUPS:
            sets['and_'].add(current_group)
        if query:
            pass
        #     chosen_metarecords, hidden = utils_core.select_records(
        #         theme=current_theme,
        #         repository=repository,
        #         query=query,
        #     )
        else:
            pass
        #     chosen_metarecords = utils_core.select_random_records(
        #         theme=current_theme,
        #         repository=repository,
        #         query=query,
        #         amount=config['items_per_page'],
        #     )

        metas = [x.uuid for x in database.get_all_metas(session)]

        paginator = Paginator(
            sequence=metas,
            current_page=current_page,
            items_per_page=25,
        )

        # note = utils_browser.get_note_on_search(len(paginator),
        #                                         time.perf_counter() - start,
        #                                         hidden)
        context = {
            'title': 'test',
            'paginator': paginator,
            'query': query_text,
            'realm_route': realm_route,
            'theme_route': theme_route,
            'group_route': group_route,
            'index_thumbnails': index_thumbnails,
            'note': '???',
            # 'directory': directory,
            # 'placeholder': utils_browser.get_placeholder(current_theme),
        }
        return flask.render_template('content.html', **context)

    @app.route(
        '/preview/<realm_route>/<theme_route>/<group_route>/<meta_uuid>'
    )
    def preview(realm_route: str, theme_route: str,
                group_route: str, meta_uuid: str):
        """Show description for a single record."""
        session = Session()
        meta = database.get_meta(session, meta_uuid) or abort(404)
        query_text = request.args.get('q', '')

        context = {
            'meta': meta,
            'note': '???',
            'query_text': query_text,
            'realm_route': realm_route,
            'theme_route': theme_route,
            'group_route': group_route,
        }
        return flask.render_template('preview.html', **context)

    @app.errorhandler(404)
    def page_not_found(exc):
        """Return not found page."""
        context = {
            # 'directory': constants.ALL_THEMES,
        }
        return flask.render_template('404.html', **context), 404

    return app
