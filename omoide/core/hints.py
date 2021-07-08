# -*- coding: utf-8 -*-

"""Type hints.
"""
from typing import NewType

__all__ = [
    'Permission',
    'RawUUID',
    'UUID',
]

RawUUID = NewType('RawUUID', str)
UUID = NewType('UUID', str)
Permission = NewType('Permission', str)
