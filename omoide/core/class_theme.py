# -*- coding: utf-8 -*-

"""Collection of groups.
"""
from dataclasses import dataclass, field
from typing import FrozenSet, List

from omoide.core.class_implicit_tag import ImplicitTag
from omoide.core.class_statistics import Statistics
from omoide.core.class_synonym import Synonym
from omoide.core.hints import Permission, UUID

__all__ = [
    'Theme',
]


# pylint: disable=R0902
@dataclass
class Theme:
    """Collection of groups.

    Main goal of theme is search enrichment.
    Theme contains synonyms that apply to every metarecord, theme contains
    implicit tags and is able to enforce additional restrictions.
    """
    uuid: UUID = ''  # unique theme identifier, starts with t_
    realm_uuid: UUID = ''  # unique realm identifier, starts with r_
    # -------------------------------------------------------------------------
    route: str = ''  # resource location
    label: str = ''  # human-readable label for entity

    # rights required to see this entity, extends original permissions
    permissions: FrozenSet[Permission] = field(default_factory=frozenset)

    implicit_tags: FrozenSet[ImplicitTag] = field(default_factory=frozenset)
    synonyms: List[Synonym] = field(default_factory=list)
    statistics: Statistics = field(default_factory=Statistics)
