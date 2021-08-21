# -*- coding: utf-8 -*-
"""Database tools used specifically by the Application.
"""
from collections import defaultdict
from contextlib import contextmanager
from typing import Optional, List

import ujson
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from omoide import search_engine
from omoide.database import models


@contextmanager
def session_scope(session_type: sessionmaker):
    """Provide a transactional scope around a series of operations."""
    session = session_type()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_meta(session: Session, meta_uuid: str) -> Optional[models.Meta]:
    """Load instance of Meta from db."""
    return session.query(models.Meta) \
        .where(models.Meta.uuid == meta_uuid).first()


def get_index(session: Session) -> search_engine.Index:
    """Load instance of Index from db."""
    metas = list(session.query(models.IndexMetas).order_by('number').all())
    all_metas = [
        search_engine.ShallowMeta(x.meta_uuid, x.number, x.path_to_thumbnail)
        for x in metas
    ]

    by_tags = defaultdict(set)
    for each in session.query(models.IndexTags).all():
        by_tags[each.tag.lower()].add(each.uuid)

    index = search_engine.Index(
        all_metas=all_metas,
        by_tags={
            tag: frozenset(uuids)
            for tag, uuids in by_tags.items()
        },
    )

    return index


def get_statistic(session: Session, active_themes: Optional[List[str]]
                  ) -> search_engine.Statistics:
    """Load statistics for given targets from db."""
    if active_themes is None:
        keys = ['stats__all_themes']
    else:
        keys = [f'stats__{x}' for x in active_themes]  # FIXME

    statistic = search_engine.Statistics()
    for key in keys:
        item = session.query(models.Helper).where(
            models.Helper.key == key).first()

        if item is not None:
            local_statistic = search_engine.Statistics.from_dict(
                source=ujson.loads(item.value)
            )
            statistic += local_statistic

    return statistic
