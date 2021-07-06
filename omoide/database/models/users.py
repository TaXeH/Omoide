# -*- coding: utf-8 -*-

"""Models.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from omoide.database import common
from omoide import constants

__alL__ = [
    'User',
]


class User(common.BaseModel):
    """User model."""
    __tablename__ = 'users'

    # primary and foreign keys
    uuid = sa.Column(sa.String(length=constants.UUID_LEN),
                     primary_key=True, nullable=False, index=True)
    # relations
    permissions = relationship('PermissionUser', back_populates='permissions')
