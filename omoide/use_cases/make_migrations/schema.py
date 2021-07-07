# -*- coding: utf-8 -*-

"""Supporting code needed for SQL commands.
"""
from typing import List

import sqlalchemy as sa

from omoide import core
from omoide.database import models


def drop_temporary_params(something: dict) -> dict:
    return {
        key: value for
        key, value in something.items()
        if not key.startswith('_')
    }


def as_sql(objects: List[dict], model_type) -> List[core.SQL]:
    """Instantiate migration commands for realms."""
    sql = []

    for each in objects:
        each = drop_temporary_params(each)
        stmt = sa.insert(model_type).values(**each)
        sql.append(core.SQL(stmt))

    return sql


def instantiate_commands(content: dict):
    """Create all needed SQL instructions."""

    def _get(key: str) -> List[dict]:
        return content.get(key, [])

    sql: List[core.SQL] = []

    sql.extend(as_sql(_get('realms'), models.Realm))
    sql.extend(as_sql(_get('themes'), models.Theme))
    sql.extend(as_sql(_get('groups'), models.Group))
    sql.extend(as_sql(_get('metas'), models.Meta))
    sql.extend(as_sql(_get('users'), models.User))

    sql.extend(as_sql(_get('permissions_realm'), models.PermissionRealm))
    sql.extend(as_sql(_get('permissions_themes'), models.PermissionTheme))
    sql.extend(as_sql(_get('permissions_groups'), models.PermissionGroup))
    sql.extend(as_sql(_get('permissions_metas'), models.PermissionMeta))
    sql.extend(as_sql(_get('permissions_users'), models.PermissionUser))

    sql.extend(as_sql(_get('tags_realms'), models.TagRealm))
    sql.extend(as_sql(_get('tags_themes'), models.TagTheme))
    sql.extend(as_sql(_get('tags_groups'), models.TagGroup))
    sql.extend(as_sql(_get('tags_metas'), models.TagMeta))
    sql.extend(as_sql(_get('synonyms'), models.Synonym))
    sql.extend(as_sql(_get('implicit_tags'), models.ImplicitTag))

    return sql
