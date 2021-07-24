# -*- coding: utf-8 -*-
"""Fast lookup tables.

Gets loaded on start of the application and
helps limiting amount of database requests.
"""
from sqlalchemy.orm import Session

from omoide.database import models


def build_indexes(session: Session) -> int:
    """Create fast lookup tables."""
    new_values = 0
    new_values += build_index_tags(session)
    new_values += build_index_permissions(session)
    new_values += build_index_thumbnails(session)
    return new_values


def build_index_tags(session: Session) -> int:
    """Create indexes for tags."""
    new_values = 0

    for meta in session.query(models.Meta).all():
        for tag in meta.tags:
            value = models.IndexTags(
                tag=tag.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

        for tag in meta.group.theme.realm.tags:
            value = models.IndexTags(
                tag=tag.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

        for tag in meta.group.theme.tags:
            value = models.IndexTags(
                tag=tag.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

        for tag in meta.group.tags:
            value = models.IndexTags(
                tag=tag.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

    session.commit()

    return new_values


def build_index_permissions(session: Session) -> int:
    """Create indexes for permissions."""
    new_values = 0

    for realm in session.query(models.Realm).all():
        for permission in realm.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=realm.uuid,
            )
            session.add(value)
            new_values += 1

    session.commit()

    for theme in session.query(models.Theme).all():
        for permission in theme.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=theme.uuid,
            )
            session.add(value)
            new_values += 1

    session.commit()

    for group in session.query(models.Group).all():
        for permission in group.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=group.uuid,
            )
            session.add(value)
            new_values += 1

    session.commit()

    for meta in session.query(models.Meta).all():
        for permission in meta.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

        for permission in meta.group.theme.realm.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

        for permission in meta.group.theme.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

        for permission in meta.group.permissions:
            value = models.IndexTags(
                tag=permission.value,
                uuid=meta.uuid,
            )
            session.add(value)
            new_values += 1

    session.commit()

    return new_values


def build_index_thumbnails(session: Session) -> int:
    """Create simplified table for thumbnail information."""
    new_values = 0

    for meta in session.query(models.Meta).all():
        value = models.IndexThumbnails(
            meta_uuid=meta.uuid,
            path_to_thumbnail=meta.path_to_thumbnail,
        )

        session.add(value)
        new_values += 1

    session.commit()

    return new_values
