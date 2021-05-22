# -*- coding: utf-8 -*-

"""Common database related utils.
"""
from typing import Set, Dict

from sqlalchemy import select, Column
from sqlalchemy.engine import Engine

from omoide import core
from omoide.database.models import base, users


def get_realms_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for realms."""
    return get_unique(database, base.realms.c.uuid)


def get_themes_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for themes."""
    return get_unique(database, base.themes.c.uuid)


def get_groups_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for groups."""
    return get_unique(database, base.groups.c.uuid)


def get_metas_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for metas."""
    return get_unique(database, base.metas.c.uuid)


def get_synonyms_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for synonyms."""
    return get_unique(database, base.synonyms.c.uuid)


def get_implicit_tags_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for implicit tags."""
    return get_unique(database, base.implicit_tags.c.uuid)


def get_users_uuids(database: Engine) -> Set[str]:
    """Get all used uuids for users."""
    return get_unique(database, users.users.c.uuid)


def get_unique(database: Engine, column: Column) -> Set[str]:
    """Return unique value of a field."""
    stmt = select(column)

    with database.begin() as conn:
        rows = conn.execute(stmt).all()

    return {x for x, in rows}


def create_uuid_mater_from_db(database: Engine,
                              aliases: Dict[str, str]) -> core.UUIDMaster:
    """Create UUIDMaster using database."""
    return core.UUIDMaster(
        aliases=aliases,
        uuids_realms=get_realms_uuids(database),
        uuids_themes=get_themes_uuids(database),
        uuids_groups=get_groups_uuids(database),
        uuids_metas=get_metas_uuids(database),
        uuids_synonyms=get_synonyms_uuids(database),
        uuids_implicit_tags=get_implicit_tags_uuids(database),
    )
