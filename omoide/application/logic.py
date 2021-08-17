# -*- coding: utf-8 -*-
"""Business logic of the service.
"""
import time
from typing import Dict, Any, Callable

from sqlalchemy.orm import sessionmaker

from omoide import constants
from omoide import search_engine
from omoide.application import appearance, navigation
from omoide.application import cache
from omoide.application import database
from omoide.application import search
from omoide.search_engine import find


# pylint: disable=too-many-locals
def make_search_response(maker: sessionmaker, web_query: search.WebQuery,
                         query_builder: search_engine.QueryBuilder,
                         index: search_engine.Index) -> Dict[str, Any]:
    """Create context for search request."""
    start = time.perf_counter()
    active_themes = []

    user_query = web_query.get('q')
    active_themes_raw = web_query.get('active_themes', constants.ALL_THEMES)
    if active_themes_raw != constants.ALL_THEMES:
        active_themes = [x.strip() for x in active_themes_raw.split(',')]

        if len(active_themes) == 1:
            current_theme = active_themes[0]
            with database.session_scope(maker) as session:
                theme_name = cache.get_theme_name(session, current_theme)
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
        if active_themes_raw != constants.ALL_THEMES:
            for theme_uuid in active_themes:
                search_query = search_query.append_and(theme_uuid)
        uuids, search_report = find.specific_records(search_query, index)
    else:
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


def make_navigation_response_get(maker: sessionmaker,
                                 web_query: search.WebQuery,
                                 current_realm: str,
                                 current_theme: str) -> Dict[str, Any]:
    """Create context for navigation request (GET)."""
    with database.session_scope(maker) as session:
        graph = cache.get_graph(session)

    user_query = web_query.get('q')
    table, highlight = navigation.get_table_with_highlight(
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
    return context


def make_navigation_response_post(maker: sessionmaker,
                                  web_query: search.WebQuery,
                                  form: dict,
                                  current_realm: str,
                                  abort_callback: Callable) -> search.WebQuery:
    """Create context for navigation request (POST)."""
    with database.session_scope(maker) as session:
        if (theme_uuid := form.get('current_theme')) is not None:
            realm_uuid = cache.get_realm_uuid_for_theme_uuid(
                session=session,
                theme_uuid=theme_uuid,
                previous_realm=current_realm,
            )

            if realm_uuid is None:
                abort_callback(404)

            web_query['current_realm'] = realm_uuid
            web_query['current_theme'] = theme_uuid

        elif (realm_uuid := form.get('current_realm')) is not None:
            web_query['current_realm'] = realm_uuid

    return web_query


def make_preview_response(maker: sessionmaker,
                          web_query: search.WebQuery,
                          uuid: str,
                          abort_callback: Callable) -> Dict[str, Any]:
    """Create context for preview request."""
    with database.session_scope(maker) as session:
        meta = database.get_meta(session, uuid) or abort_callback(404)

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
