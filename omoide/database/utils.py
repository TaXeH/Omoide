# -*- coding: utf-8 -*-

"""Common database related utils.
"""
from typing import Set, Type

from sqlalchemy.orm import Session

import omoide.database.models.relations
from omoide.database import common
from omoide.database import models


def get_realms_uuids(session: Session) -> Set[str]:
    """Get all used uuids for realms."""
    return get_unique_uuids(session, models.Realm)


def get_themes_uuids(session: Session) -> Set[str]:
    """Get all used uuids for themes."""
    return get_unique_uuids(session, models.Theme)


def get_groups_uuids(session: Session) -> Set[str]:
    """Get all used uuids for groups."""
    return get_unique_uuids(session, models.Group)


def get_metas_uuids(session: Session) -> Set[str]:
    """Get all used uuids for metas."""
    return get_unique_uuids(session, models.Meta)


def get_synonyms_uuids(session: Session) -> Set[str]:
    """Get all used uuids for synonyms."""
    return get_unique_uuids(session, omoide.database.models.relations.Synonym)


def get_implicit_tags_uuids(session: Session) -> Set[str]:
    """Get all used uuids for implicit tags."""
    return get_unique_uuids(session,
                            omoide.database.models.relations.ImplicitTag)


def get_users_uuids(session: Session) -> Set[str]:
    """Get all used uuids for users."""
    return get_unique_uuids(session, models.User)


def get_unique_uuids(session: Session,
                     model: Type[common.BaseModel]) -> Set[str]:
    """Return unique value of a field."""
    return {
        each.uuid for each in session.query(model).all()
    }
