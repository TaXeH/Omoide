# -*- coding: utf-8 -*-
"""Caching tools.
"""
from typing import Dict, Type, Optional

from sqlalchemy.orm import Session

from omoide import constants
from omoide.database import models

_sentinel = object()
_REALM_NAMES_CACHE: Dict[str, str] = {}
_THEME_UUIDS_TO_REALMS_UUIDS_CACHE: Dict[str, Optional[str]] = {}
_THEME_NAMES_CACHE: Dict[str, str] = {}


def get_theme_name(session: Session, theme_uuid: str) -> str:
    """Return cached or find theme name by uuid."""
    if theme_uuid == constants.ALL_THEMES:
        return ''
    return _common_getter(session, theme_uuid,
                          _THEME_NAMES_CACHE, models.Theme)


def _common_getter(session: Session, uuid: str, collection: Dict[str, str],
                   model: Type[models.Theme]
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
