# -*- coding: utf-8 -*-

"""Core models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide import constants
from omoide.database import common

__alL__ = [
    'Realm',
    'Theme',
    'Group',
    'Meta',
]


class Realm(common.BaseModel):
    """Realm model."""
    __tablename__ = 'realms'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    # fields
    route = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    label = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    themes = relationship('Theme', back_populates='realm')
    tags = relationship('RealmTag', back_populates='realm')
    permissions = relationship('PermissionRealm', back_populates='permissions')


class Theme(common.BaseModel):
    """Theme model."""
    __tablename__ = 'themes'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    realm_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('realms.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    route = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    label = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    realm = relationship('Realm', back_populates='themes')
    groups = relationship('Group', back_populates='theme')
    tags = relationship('ThemeTag', back_populates='theme')
    synonyms = relationship('Synonym', back_populates='theme')
    implicit_tags = relationship('ImplicitTag', back_populates='theme')
    permissions = relationship('PermissionTheme', back_populates='permissions')


class Group(common.BaseModel):
    """Group model."""
    __tablename__ = 'groups'

    # primary and foreign keys
    # unique group identifier, starts with g_
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    # unique theme identifier, starts with t_
    theme_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    # resource location
    route = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    # human-readable label for entity
    label = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # information about origin
    # metarecord values are more important than these
    # date of registration in form '2021-01-01'
    registered_on = sa.Column(sa.String(length=constants.DATE_LEN),
                              nullable=False, server_default='')
    # uuid of user or ''
    registered_by = sa.Column(sa.String(length=constants.MAX_LEN),
                              nullable=False, server_default='')
    # name of the author
    author = sa.Column(sa.String(length=constants.MAX_LEN),
                       nullable=False, server_default='')
    # link to author's page or account
    author_url = sa.Column(sa.Text, nullable=False, server_default='')
    # link to the page where this content was seen
    origin_url = sa.Column(sa.Text, nullable=False, server_default='')
    # optional description of the entity
    comment = sa.Column(sa.Text, nullable=False, server_default='')

    # string with arbitrary names, that represent some logical structure
    # supposed to be used in ordering, like 'plants,flowers,daisy'
    hierarchy = sa.Column(sa.Text,
                          nullable=False, server_default='')

    # relations
    theme = relationship('Theme', back_populates='groups')
    metas = relationship('Meta', back_populates='group')
    tags = relationship('GroupTag', back_populates='group')
    permissions = relationship('PermissionGroup', back_populates='permissions')


class Meta(common.BaseModel):
    """Metarecord of a single item in the storage.

    Minimal unit of storage. Stores all info about one specific file.
    """
    __tablename__ = 'metas'

    # primary and foreign keys
    # unique meta identifier, starts with m_
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False)
    # unique group identifier, starts with g_
    group_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('groups.uuid'),
                           nullable=False, unique=False)
    # fields
    # path to actual files, relative to theme directory
    path_to_content = sa.Column(sa.Text, nullable=False, server_default='0')
    path_to_preview = sa.Column(sa.Text, nullable=False, server_default='0')
    path_to_thumbnail = sa.Column(sa.Text, nullable=False, server_default='0')

    # original file parameters, can indirectly help in sorting
    # like 'somefile', without extension and dot
    original_filename = sa.Column(sa.Text, nullable=False, server_default='0')
    # like 'jpg', without dot
    original_extension = sa.Column(sa.String(length=constants.MAX_LEN),
                                   nullable=False, server_default='0')
    # specific content information
    # in pixels for images, 0 for everything else
    width = sa.Column(sa.Integer, nullable=False, server_default='0')
    # in pixels for images, 0 for everything else
    height = sa.Column(sa.Integer, nullable=False, server_default='0')
    # in megapixels for images, 0 for everything else
    resolution = sa.Column(sa.Float, nullable=False, server_default='0')
    # in bytes for any file
    size = sa.Column(sa.Integer, nullable=False, server_default='0')
    # in seconds for video and audio, 0 for everything else
    duration = sa.Column(sa.Integer, nullable=False, server_default='0')
    # string like 'image', 'video', etc.
    type = sa.Column(sa.String(length=constants.MAX_LEN),
                     nullable=False, server_default='')

    # used in group handling, some arbitrary number, that helps in sorting
    ordering = sa.Column(sa.Integer, nullable=False, server_default='0')

    # information about origin
    # metarecord values are more important than these
    # date of registration in form '2021-01-01'
    registered_on = sa.Column(sa.String(length=constants.DATE_LEN),
                              nullable=False, server_default='')
    # uuid of user or ''
    registered_by = sa.Column(sa.String(length=constants.MAX_LEN),
                              nullable=False, server_default='')
    # name of the author
    author = sa.Column(sa.String(length=constants.MAX_LEN),
                       nullable=False, server_default='')
    # link to author's page or account
    author_url = sa.Column(sa.Text, nullable=False, server_default='')
    # link to the page where this content was seen
    origin_url = sa.Column(sa.Text, nullable=False, server_default='')
    # optional description of the entity
    comment = sa.Column(sa.Text, nullable=False, server_default='')

    # identification info
    # encoded signature string
    signature = sa.Column(sa.Text, nullable=False, server_default='')
    # human-readable type, like 'md5'
    signature_type = sa.Column(sa.Text, nullable=False, server_default='')

    # uuid of the previous meta
    previous = sa.Column(sa.Text, nullable=False, server_default='')
    # uuid of the next meta
    next = sa.Column(sa.Text, nullable=False, server_default='')

    # string with arbitrary names, that represent some logical structure
    # supposed to be used in ordering, like 'plants,flowers,daisy'
    hierarchy = sa.Column(sa.Text, nullable=False, server_default='')

    # relations
    group = relationship('Group', back_populates='metas')
    tags = relationship('MetaTag', back_populates='meta')
    permissions = relationship('PermissionMeta', back_populates='permissions')
