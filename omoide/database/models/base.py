# -*- coding: utf-8 -*-

"""Models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide.database import common
from omoide.database import constants

__alL__ = [
    'Realm',
    'Theme',
    'Group',
    'Meta',
    'ImplicitTag',
    'Synonym',
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
    permissions = relationship('PermissionTheme', back_populates='permissions')


class Group(common.BaseModel):
    """Group model."""
    __tablename__ = 'groups'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    theme_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    route = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    label = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    registered_on = sa.Column(sa.String(length=constants.DATE_LEN),
                              nullable=False)
    registered_by = sa.Column(sa.String(length=constants.MAX_LEN),
                              nullable=False)
    author = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    author_url = sa.Column(sa.Text, nullable=False)
    origin_url = sa.Column(sa.Text, nullable=False)
    comment = sa.Column(sa.Text, nullable=False)
    hierarchy = sa.Column(sa.Text, nullable=False)

    # relations
    theme = relationship('Theme', back_populates='groups')
    metas = relationship('Meta', back_populates='group')
    tags = relationship('GroupTag', back_populates='group')
    permissions = relationship('PermissionGroup', back_populates='permissions')


class Meta(common.BaseModel):
    """Meta model."""
    __tablename__ = 'metas'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False)
    group_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('groups.uuid'),
                           nullable=False, unique=False)
    # fields
    path_to_content = sa.Column(sa.Text, nullable=False)
    path_to_preview = sa.Column(sa.Text, nullable=False)
    path_to_thumbnail = sa.Column(sa.Text, nullable=False)
    original_filename = sa.Column(sa.Text, nullable=False)
    original_extension = sa.Column(sa.String(length=constants.MAX_LEN),
                                   nullable=False)
    width = sa.Column(sa.Integer, nullable=False)
    height = sa.Column(sa.Integer, nullable=False)
    resolution = sa.Column(sa.Float, nullable=False)
    size = sa.Column(sa.Integer, nullable=False)
    duration = sa.Column(sa.Integer, nullable=False)
    type = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    ordering = sa.Column(sa.Integer, nullable=False)
    registered_on = sa.Column(sa.String(length=constants.DATE_LEN),
                              nullable=False)
    registered_by = sa.Column(sa.String(length=constants.MAX_LEN),
                              nullable=False)
    author = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)
    author_url = sa.Column(sa.Text, nullable=False)
    origin_url = sa.Column(sa.Text, nullable=False)
    comment = sa.Column(sa.Text, nullable=False)
    signature = sa.Column(sa.Text, nullable=False)
    signature_type = sa.Column(sa.Text, nullable=False)
    previous = sa.Column(sa.Text, nullable=False)
    next = sa.Column(sa.Text, nullable=False)
    hierarchy = sa.Column(sa.Text, nullable=False)

    # relations
    group = relationship('Group', back_populates='metas')
    tags = relationship('MetaTag', back_populates='meta')
    permissions = relationship('PermissionMeta', back_populates='permissions')


class Synonym(common.BaseModel):
    """Synonym model."""
    __tablename__ = 'synonyms'

    # primary and foreign keys
    uuid = sa.Column('uuid', sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    theme_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    description = sa.Column('description', sa.Text, nullable=False)

    # relations
    values = relationship('SynonymValue', back_populates='synonym')


class ImplicitTag(common.BaseModel):
    """Implicit tag model."""
    __tablename__ = 'implicit_tags'

    # primary and foreign keys
    uuid = sa.Column('uuid', sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    theme_uuid = sa.Column('theme_uuid', sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    description = sa.Column('description', sa.Text, nullable=False)

    # relations
    values = relationship('ImplicitTagValue', back_populates='implicit_tag')
