# -*- coding: utf-8 -*-

"""Models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide.database import common
from omoide.database import constants

__alL__ = [
    'PermissionRealm',
    'PermissionTheme',
    'PermissionGroup',
    'PermissionMeta',
    'PermissionUser',
]


class PermissionRealm(common.BaseModel):
    """Permission for realm model."""
    __tablename__ = 'permissions_realms'

    # primary and foreign keys
    realm_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('realms.uuid'),
                           primary_key=True, nullable=False,
                           unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    realm = relationship('Realm', back_populates='permissions')


class PermissionTheme(common.BaseModel):
    """Permission for theme model."""
    __tablename__ = 'permissions_themes'

    # primary and foreign keys
    theme_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('themes.uuid'),
                           primary_key=True, nullable=False,
                           unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    realm = relationship('Theme', back_populates='permissions')


class PermissionGroup(common.BaseModel):
    """Permission for group model."""
    __tablename__ = 'permissions_groups'

    # primary and foreign keys
    group_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                           sa.ForeignKey('groups.uuid'),
                           primary_key=True, nullable=False, unique=False)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    group = relationship('Group', back_populates='permissions')


class PermissionMeta(common.BaseModel):
    """Permission for meta model."""
    __tablename__ = 'permissions_metas'

    # primary and foreign keys
    meta_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                          sa.ForeignKey('metas.uuid'),
                          primary_key=True, nullable=False,
                          unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    realm = relationship('Meta', back_populates='permissions')


class PermissionUser(common.BaseModel):
    """Permission for user model."""
    __tablename__ = 'permissions_users'

    # primary and foreign keys
    user_uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                          sa.ForeignKey('users.uuid'),
                          primary_key=True, nullable=False,
                          unique=False, index=True)
    # fields
    value = sa.Column('value', sa.String(length=constants.MAX_LEN),
                      nullable=False)
    # relations
    realm = relationship('User', back_populates='permissions')
