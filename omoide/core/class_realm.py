# -*- coding: utf-8 -*-

"""Collection of themes.
"""
from dataclasses import dataclass, field
from typing import FrozenSet

from omoide.core.class_statistics import Statistics
from omoide.core.hints import Permission, UUID

__all__ = [
    'Realm',
]


# pylint: disable=R0902
@dataclass
class Realm:
    """Collection of themes.

    Main goal of realm is access control.
    Realms are supposed to be connected to their owner.
    All themes inside inherit current realm permissions.
    """
    uuid: UUID = ''  # unique realm identifier, starts with r_
    # -------------------------------------------------------------------------
    route: str = ''  # resource location
    label: str = ''  # human-readable label for entity

    # rights required to see this entity, extends original permissions
    permissions: FrozenSet[Permission] = field(default_factory=frozenset)
    statistics: Statistics = field(default_factory=Statistics)
