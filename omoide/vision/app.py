import flask
from sqlalchemy.engine import Engine


def create_app(templates: str, static: str, engine: Engine) -> flask.Flask:
    app = flask.Flask(
        import_name='omoide',
        template_folder=templates,
        static_folder=static,
    )

    @app.route('/')
    def index():
        """Entry page.

        Redirects user to path with default directory.
        """
        return 'ok'
        # return flask.redirect(
        #     url_for('index_all', directory=constants.ALL_THEMES)
        # )

    @app.route('/index/<directory>/', methods=['GET', 'POST'])
    @app.route('/index/<directory>/search', methods=['GET', 'POST'])
    def index_all(directory: str):
        """Main page of the script."""
        # if request.method == 'POST':
        #     return utils_browser.add_query_to_path(request, directory)

        # start = time.perf_counter()
        # query_text = request.args.get('q', '')
        # current_page = int(request.args.get('page', 1))
        # current_theme = themes_repository.get(directory) or abort(404)
        # query = query_builder.from_query(query_text, directory)
        # hidden = 0
        #
        # if query:
        #     chosen_metarecords, hidden = utils_core.select_records(
        #         theme=current_theme,
        #         repository=repository,
        #         query=query,
        #     )
        # else:
        #     chosen_metarecords = utils_core.select_random_records(
        #         theme=current_theme,
        #         repository=repository,
        #         query=query,
        #         amount=config['items_per_page'],
        #     )
        #
        # paginator = Paginator(
        #     sequence=chosen_metarecords,
        #     current_page=current_page,
        #     items_per_page=config['items_per_page'],
        # )
        #
        # note = utils_browser.get_note_on_search(len(paginator),
        #                                         time.perf_counter() - start,
        #                                         hidden)
        context = {
            'title': 'test',
            # 'paginator': paginator,
            # 'query': query_text,
            # 'note': note,
            # 'directory': directory,
            # 'placeholder': utils_browser.get_placeholder(current_theme),
        }
        return flask.render_template('content.html', **context)

    @app.errorhandler(404)
    def page_not_found(exc):
        """Return not found page."""
        print(exc)
        context = {
            # 'directory': constants.ALL_THEMES,
        }
        return flask.render_template('404.html', **context), 404

    return app
