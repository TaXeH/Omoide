# -*- coding: utf-8 -*-

"""Type hints.
"""
from typing import NewType

__all__ = [
    'Permission',
    'UUID',
]

UUID = NewType('UUID', str)
Permission = NewType('Permission', str)
