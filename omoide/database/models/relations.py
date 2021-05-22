# -*- coding: utf-8 -*-

"""Models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide.database import common
from omoide.database import constants

__all__ = [
    'RealmTag',
    'ThemeTag',
    'GroupTag',
    'MetaTag',
    'SynonymValue',
    'ImplicitTagValue',
]


class RealmTag(common.BaseModel):
    """Realm tag model."""
    __tablename__ = 'tags_realms'

    # primary and foreign keys
    realm_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('realms.uuid'),
                           primary_key=True, nullable=False,
                           unique=False, index=True)
    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    realm = relationship('Realm', back_populates='tags')


class ThemeTag(common.BaseModel):
    """Theme tag model."""
    __tablename__ = 'tags_themes'

    # primary and foreign keys
    theme_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           primary_key=True, nullable=False,
                           unique=False, index=True)
    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    theme = relationship('Theme', back_populates='tags')


class GroupTag(common.BaseModel):
    """Group tag model."""
    __tablename__ = 'tags_groups'

    # primary and foreign keys
    group_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('groups.uuid'),
                           primary_key=True, nullable=False,
                           unique=False, index=True)

    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    group = relationship('Group', back_populates='tags')


class MetaTag(common.BaseModel):
    """Meta tag model."""
    __tablename__ = 'tags_metas'

    # primary and foreign keys
    meta_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                          sa.ForeignKey('metas.uuid'),
                          primary_key=True, nullable=False,
                          unique=False, index=True)

    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    meta = relationship('Meta', back_populates='tags')


class SynonymValue(common.BaseModel):
    """Single synonym value model."""
    __tablename__ = 'synonyms_values'

    # primary and foreign keys
    implicit_tag_uuid = sa.Column('synonym_uuid',
                                  sa.String(length=constants.UUID_LEN),
                                  sa.ForeignKey('synonyms.uuid'),
                                  primary_key=True, nullable=False,
                                  unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    synonym = relationship('Synonym', back_populates='values')


class ImplicitTagValue(common.BaseModel):
    """Single implicit tag value model."""
    __tablename__ = 'implicit_tags_values'

    # primary and foreign keys
    implicit_tag_uuid = sa.Column('implicit_tag_uuid',
                                  sa.String(length=constants.UUID_LEN),
                                  sa.ForeignKey('implicit_tags.uuid'),
                                  primary_key=True, nullable=False,
                                  unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    implicit_tag = relationship('ImplicitTag', back_populates='values')
