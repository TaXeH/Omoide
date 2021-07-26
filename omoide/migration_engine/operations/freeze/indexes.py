# -*- coding: utf-8 -*-
"""Fast lookup tables.

Gets loaded on start of the application and
helps limiting amount of database requests.
"""
from sqlalchemy.orm import Session

from omoide.database import models

_META_REALMS_CACHE = {}
_META_THEMES_CACHE = {}
_META_GROUPS_CACHE = {}


def build_indexes(session: Session) -> int:
    """Create fast lookup tables."""
    new_values = 0
    new_values += build_index_tags(session)
    new_values += build_index_permissions(session)
    new_values += build_index_meta(session)
    # TODO - add search enhancements
    return new_values


def lazy_get_realm(meta: models.Meta) -> models.Realm:
    """Lazy return Realm or go to database for it."""
    value = _META_REALMS_CACHE.get(meta.uuid)

    if value is None:
        value = meta.group.theme.realm
        _META_REALMS_CACHE[meta.uuid] = value

    return value


def lazy_get_theme(meta: models.Meta) -> models.Theme:
    """Lazy return Theme or go to database for it."""
    value = _META_THEMES_CACHE.get(meta.uuid)

    if value is None:
        value = meta.group.theme
        _META_THEMES_CACHE[meta.uuid] = value

    return value


def lazy_get_group(meta: models.Meta) -> models.Group:
    """Lazy return Group or go to database for it."""
    value = _META_GROUPS_CACHE.get(meta.uuid)

    if value is None:
        value = meta.group
        _META_GROUPS_CACHE[meta.uuid] = value

    return value


def build_index_tags(session: Session) -> int:
    """Create indexes for tags."""
    new_values = 0

    for meta in session.query(models.Meta).all():
        realm = lazy_get_realm(meta)
        theme = lazy_get_theme(meta)
        group = lazy_get_group(meta)

        all_tags = {
            *(x.value for x in realm.tags),
            *(x.value for x in theme.tags),
            *(x.value for x in group.tags),
            *(x.value for x in meta.tags),
        }
        new_values += len(all_tags)

        for tag in all_tags:
            value = models.IndexTags(tag=tag, uuid=meta.uuid)
            session.add(value)

    session.commit()

    return new_values


def build_index_permissions(session: Session) -> int:
    """Create indexes for permissions."""
    new_values = 0

    for meta in session.query(models.Meta).all():
        realm = lazy_get_realm(meta)
        theme = lazy_get_theme(meta)
        group = lazy_get_group(meta)

        all_permissions = {
            *(x.value for x in realm.permissions),
            *(x.value for x in theme.permissions),
            *(x.value for x in group.permissions),
            *(x.value for x in meta.permissions),
        }
        new_values += len(all_permissions)

        for tag in all_permissions:
            value = models.IndexPermissions(permission=tag, uuid=meta.uuid)
            session.add(value)

    session.commit()

    return new_values


def build_index_meta(session: Session) -> int:
    """Create simplified table for thumbnail information."""
    all_metas = list(session.query(models.Meta).all())
    new_values = len(all_metas)

    all_metas.sort(key=lambda meta: (meta.hierarchy, meta.ordering))

    for i, each_meta in enumerate(all_metas):
        value = models.IndexMetas(
            meta_uuid=each_meta.uuid,
            number=i,
            path_to_thumbnail=each_meta.path_to_thumbnail,
        )
        session.add(value)

    session.commit()

    return new_values
