# -*- coding: utf-8 -*-
"""Business logic of the service.
"""
import time
from typing import Dict, Any, Callable

from sqlalchemy.orm import sessionmaker

from omoide import constants
from omoide.application import appearance, navigation
from omoide.application import cache
from omoide.application import database
from omoide.application import search
from omoide.application.search import search_routine


def make_search_response(maker: sessionmaker, web_query: search.WebQuery,
                         query_builder: search.QueryBuilder,
                         index: search.Index) -> Dict[str, Any]:
    """Create context for search request."""
    start = time.perf_counter()

    current_realm = web_query.get('current_realm', constants.ALL_REALMS)
    current_theme = web_query.get('current_theme', constants.ALL_THEMES)

    with database.session_scope(maker) as session:
        realm_name = cache.get_realm_name(session, current_realm)
        theme_name = cache.get_theme_name(session, current_theme)

    user_query = web_query.get('q')
    current_page = int(web_query.get('page', '1'))

    query = query_builder.from_query(user_query)

    if current_realm != constants.ALL_REALMS:
        query.and_.add(current_realm)

    if current_theme != constants.ALL_THEMES:
        query.and_.add(current_theme)

    if query:
        uuids = search_routine.find_records(query, index, 15)
    else:
        uuids = search_routine.random_records(index, 15)

    paginator = search.Paginator(
        sequence=uuids,
        current_page=current_page,
        items_per_page=15,  # FIXME
    )

    duration = time.perf_counter() - start
    note = appearance.get_note_on_search(len(paginator), duration)

    context = {
        'web_query': web_query,
        'user_query': user_query,
        'paginator': paginator,
        'note': note,
        'placeholder': appearance.get_placeholder(realm_name, theme_name),
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
            *[x.value for x in meta.group.theme.realm.tags],
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
