# -*- coding: utf-8 -*-

"""Models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide import constants
from omoide.database import common

__alL__ = [
    'User',
]


class User(common.BaseModel):
    """User model."""
    __tablename__ = 'users'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    # fields
    name = sa.Column('value', sa.String(length=constants.MAX_LEN),
                     nullable=False)
    # relations
    permissions = relationship('PermissionUser', back_populates='user')
