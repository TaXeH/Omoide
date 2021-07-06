# -*- coding: utf-8 -*-

"""Index models.
"""
import sqlalchemy as sa

from omoide import constants
from omoide.database import common

__alL__ = [
    'IndexTags',
    'IndexPermissions',
    'IndexThumbnails',
]


class IndexTags(common.BaseModel):
    """Index for tags info.

    Used to perform fast search on tags. Note that we're not limiting tag
    column with existing tags and uuid column with existing uuids.
    Gets loaded at the application start and never queried after.
    """
    __tablename__ = 'index_tags'

    # primary and foreign keys
    id = sa.Column(sa.Integer,
                   primary_key=True, unique=True, autoincrement=True)
    # fields
    tag = sa.Column(sa.String(length=constants.MAX_LEN),
                    nullable=False, unique=False, index=True)
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     nullable=False, unique=False)


class IndexPermissions(common.BaseModel):
    """Index for permissions info.

    Used to perform fast search on permissions. Note that we're not limiting
    permission column with existing permissions and uuid column with existing
    uuids. Gets loaded at the application start and never queried after.
    """
    __tablename__ = 'index_permissions'

    # primary and foreign keys
    id = sa.Column(sa.Integer,
                   primary_key=True, unique=True, autoincrement=True)
    # fields
    permission = sa.Column(sa.String(length=constants.MAX_LEN),
                           nullable=False, unique=False, index=True)
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     nullable=False, unique=False)


class IndexThumbnails(common.BaseModel):
    """Index for thumbnail info.

    Fast access to the thumbnail info without need to go to the database.
    Gets loaded at the application start and never queried after.
    """
    __tablename__ = 'index_thumbnails'

    # primary and foreign keys
    meta_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                          sa.ForeignKey('metas.uuid'),
                          primary_key=True, nullable=False,
                          unique=True, index=True)
    # fields
    path_to_thumbnail = sa.Column(sa.Text, nullable=False)
