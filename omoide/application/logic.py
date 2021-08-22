# -*- coding: utf-8 -*-
"""Business logic of the service.
"""
import time
from typing import Dict, Any, Callable, List, Optional

import ujson
from sqlalchemy.orm import sessionmaker

from omoide import constants
from omoide import search_engine
from omoide.application import appearance
from omoide.application import database as app_database
from omoide.application import search
from omoide.database import operations
from omoide.search_engine import find


# pylint: disable=too-many-locals
def make_search_response(maker: sessionmaker, web_query: search.WebQuery,
                         query_builder: search_engine.QueryBuilder,
                         index: search_engine.Index) -> Dict[str, Any]:
    """Create context for search request."""
    start = time.perf_counter()

    user_query = web_query.get('q')

    active_themes_raw = web_query.get('active_themes', constants.ALL_THEMES)
    active_themes_string = web_query.get('active_themes', constants.ALL_THEMES)
    active_themes = appearance.extract_active_themes(active_themes_string)

    if active_themes is not None:
        if len(active_themes) == 1:
            current_theme = active_themes[0]
            with operations.session_scope(maker) as session:
                theme_name = app_database.get_theme_name(
                    session, current_theme)
            placeholder = 'Searching on theme {}'.format(repr(theme_name))
        elif len(active_themes) > 1:
            placeholder = 'Searching on {}-x themes'.format(len(active_themes))
        else:
            placeholder = 'No active theme'
            user_query = ''
    else:
        placeholder = ''

    current_page = int(web_query.get('page', '1'))
    search_query = query_builder.from_query(user_query)

    if search_query:
        if active_themes is not None:
            for theme_uuid in active_themes:
                search_query = search_query.append_and(theme_uuid)
        uuids, search_report = find.specific_records(search_query, index)
    else:
        # TODO - add theme filtering
        uuids = find.random_records(index, 50)
        search_report = []

    paginator = search.Paginator(
        sequence=uuids,
        current_page=current_page,
        items_per_page=50,  # FIXME
    )

    duration = time.perf_counter() - start
    note = appearance.get_note_on_search(len(paginator), duration)

    context = {
        'web_query': web_query,
        'user_query': user_query,
        'search_query': search_query,
        'paginator': paginator,
        'search_report': search_report,
        'note': note,
        'placeholder': placeholder,
    }
    return context


def make_navigation_response(maker: sessionmaker,
                             web_query: search.WebQuery,
                             active_themes: Optional[List[str]],
                             ) -> Dict[str, Any]:
    """Create context for navigation request (GET)."""
    with operations.session_scope(maker) as session:
        graph = app_database.get_graph(session)

    user_query = web_query.get('q')

    if active_themes is None:
        visibility = {x: True for x in graph}
    else:
        _active_themes = set(active_themes)
        visibility = {x: x in active_themes for x in graph}

    context = {
        'web_query': web_query,
        'user_query': user_query,
        'graph': graph,
        'visibility': visibility,
        'visibility_json': ujson.dumps(visibility),
    }
    return context


def make_preview_response(maker: sessionmaker,
                          web_query: search.WebQuery,
                          uuid: str,
                          abort_callback: Callable) -> Dict[str, Any]:
    """Create context for preview request."""
    with operations.session_scope(maker) as session:
        meta = app_database.get_meta(session, uuid) or abort_callback(404)

        all_tags = {
            *[x.value for x in meta.group.theme.tags],
            *[x.value for x in meta.group.tags],
            *[x.value for x in meta.tags],
        }
        session.expunge_all()

    context = {
        'web_query': web_query,
        'meta': meta,
        'tags': sorted(all_tags),
    }
    return context
