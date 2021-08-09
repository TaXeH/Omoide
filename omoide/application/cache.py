# -*- coding: utf-8 -*-
"""Caching tools.
"""
import json
from typing import Dict, Union, Type, Optional

from sqlalchemy.orm import Session

from omoide import constants
from omoide.database import models

_sentinel = object()
_REALM_NAMES_CACHE: Dict[str, str] = {}
_THEME_UUIDS_TO_REALMS_UUIDS_CACHE: Dict[str, Optional[str]] = {}
_THEME_NAMES_CACHE: Dict[str, str] = {}
_GRAPH_CACHE: Optional[dict] = None


def get_realm_name(session: Session, realm_uuid: str) -> str:
    """Return cached or find realm name by uuid."""
    if realm_uuid == constants.ALL_REALMS:
        return ''
    return _common_getter(session, realm_uuid,
                          _REALM_NAMES_CACHE, models.Realm)


def get_theme_name(session: Session, theme_uuid: str) -> str:
    """Return cached or find theme name by uuid."""
    if theme_uuid == constants.ALL_THEMES:
        return ''
    return _common_getter(session, theme_uuid,
                          _THEME_NAMES_CACHE, models.Theme)


def _common_getter(session: Session, uuid: str, collection: Dict[str, str],
                   model: Union[Type[models.Realm], Type[models.Theme]]
                   ) -> str:
    """Return cached or find in database."""
    value = collection.get(uuid)

    if value is not None:
        return value

    response = session.query(model).where(model.uuid == uuid).first()

    if response is not None:
        value = response.label
        collection[uuid] = value
        return value

    return constants.UNKNOWN


def get_realm_uuid_for_theme_uuid(session: Session,
                                  theme_uuid: str,
                                  previous_realm: str) -> Optional[str]:
    """Return UUID for realm which holds this theme."""
    if theme_uuid == constants.ALL_THEMES:
        return previous_realm

    value = _THEME_UUIDS_TO_REALMS_UUIDS_CACHE.get(theme_uuid, _sentinel)

    if value is not _sentinel:
        return value

    theme = session.query(models.Theme) \
        .where(models.Theme.uuid == theme_uuid).first()

    if theme is None:
        _THEME_UUIDS_TO_REALMS_UUIDS_CACHE[theme_uuid] = None
        return None

    uuid = theme.realm.uuid
    _THEME_UUIDS_TO_REALMS_UUIDS_CACHE[theme_uuid] = uuid
    return uuid


def get_graph(session: Session) -> dict:
    """Load site map as a graph from db."""
    global _GRAPH_CACHE

    if _GRAPH_CACHE is not None:
        return _GRAPH_CACHE

    text = session.query(models.Helper).where(
        models.Helper.key == 'graph').one().value

    body = json.loads(text)
    _GRAPH_CACHE = body

    return body
