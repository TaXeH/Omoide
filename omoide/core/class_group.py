# -*- coding: utf-8 -*-

"""Group of one or more metarecords.
"""
from dataclasses import dataclass, field
from typing import FrozenSet, List

from omoide.core.class_meta import Meta
from omoide.core.class_statistics import Statistics
from omoide.core.hints import UUID, Permission

__all__ = [
    'Group',
]


# pylint: disable=R0902,R0801
@dataclass
class Group:
    """Group of one or more metarecords.

    Main goal of group is search enrichment and record binding.
    Group allows to write common parameters in one place.
    """
    uuid: UUID = ''  # unique group identifier, starts with g_
    realm_uuid: UUID = ''  # unique realm identifier, starts with r_
    theme_uuid: UUID = ''  # unique theme identifier, starts with t_

    route: str = ''  # resource location
    label: str = ''  # human-readable label for entity

    # information about origin ------------------------------------------------
    # metarecord values are more important than these
    registered_on: str = ''  # date of registration in form '2021-01-01'
    registered_by: str = ''  # uuid of user
    author: str = ''  # name of the author
    author_url: str = ''  # link to author's page or account
    origin_url: str = ''  # link to the page where this content was seen
    comment: str = ''  # optional description of the entity

    # string with arbitrary names, that represent some logical structure
    # supposed to be used in ordering, like 'plants,flowers,daisy'
    hierarchy: str = ''

    # rights required to see this entity, extends original permissions
    permissions: FrozenSet[Permission] = field(default_factory=frozenset)
    members: List[Meta] = field(default_factory=list)
    statistics: Statistics = field(default_factory=Statistics)

    # tags of the entity
    tags: FrozenSet[str] = field(default_factory=frozenset)
