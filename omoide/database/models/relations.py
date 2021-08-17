# -*- coding: utf-8 -*-

"""Models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide import constants
from omoide.database import common

__all__ = [
    'TagTheme',
    'TagGroup',
    'TagMeta',
    'Synonym',
    'SynonymValue',
]


class TagTheme(common.BaseModel):
    """Theme tag model."""
    __tablename__ = 'tags_themes'

    # primary and foreign keys
    id = sa.Column(sa.Integer,
                   primary_key=True, unique=True, autoincrement=True)
    theme_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    theme = relationship('Theme', back_populates='tags')


class TagGroup(common.BaseModel):
    """Group tag model."""
    __tablename__ = 'tags_groups'

    # primary and foreign keys
    id = sa.Column(sa.Integer,
                   primary_key=True, unique=True, autoincrement=True)
    group_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('groups.uuid'),
                           nullable=False, unique=False, index=True)
    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    group = relationship('Group', back_populates='tags')


class TagMeta(common.BaseModel):
    """Meta tag model."""
    __tablename__ = 'tags_metas'

    # primary and foreign keys
    id = sa.Column(sa.Integer,
                   primary_key=True, unique=True, autoincrement=True)
    meta_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                          sa.ForeignKey('metas.uuid'),
                          nullable=False, unique=False, index=True)
    # fields
    value = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    meta = relationship('Meta', back_populates='tags')


class Synonym(common.BaseModel):
    """Synonym model."""
    __tablename__ = 'synonyms'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    # fields
    label = sa.Column(sa.String(length=constants.MAX_LEN), nullable=False)

    # relations
    values = relationship('SynonymValue', back_populates='synonym')


class SynonymValue(common.BaseModel):
    """Single synonym value model."""
    __tablename__ = 'synonyms_values'

    # primary and foreign keys
    id = sa.Column(sa.Integer,
                   primary_key=True, unique=True, autoincrement=True)
    synonym_uuid = sa.Column('synonym_uuid',
                             sa.String(length=constants.UUID_LEN),
                             sa.ForeignKey('synonyms.uuid'),
                             nullable=False,
                             unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    synonym = relationship('Synonym', back_populates='values')
