# -*- coding: utf-8 -*-

"""Metarecord of a single item in the storage.
"""
from dataclasses import dataclass, field
from typing import FrozenSet

from omoide.core.hints import UUID, Permission

__all__ = [
    'Meta',
]


# pylint: disable=R0902,R0801
@dataclass
class Meta:
    """Metarecord of a single item in the storage.

    Minimal unit of storage. Stores all info about one specific file.
    """
    uuid: UUID = ''  # unique meta identifier, has no prefix, starts with m_

    realm_uuid: UUID = ''  # unique realm identifier, starts with r_
    theme_uuid: UUID = ''  # unique theme identifier, starts with t_
    group_uuid: UUID = ''  # unique group identifier, starts with g_

    # path to actual files, relative to theme directory
    path_to_content: str = ''
    path_to_preview: str = ''
    path_to_thumbnail: str = ''

    # original file parameters, can indirectly help in sorting
    original_filename: str = ''  # like 'somefile', without extension and dot
    original_extension: str = ''  # like 'jpg', without dot

    # specific content information
    width: int = 0  # in pixels for images, 0 for everything else
    height: int = 0  # in pixels for images, 0 for everything else
    resolution: float = 0.0  # in megapixels for images, 0 for everything else
    size: int = 0  # in bytes for any files
    duration: int = 0  # in seconds for video and audio, 0 for everything else
    type: str = ''  # string like 'image', 'video', etc.

    # used in group handling, some arbitrary number, that helps in sorting
    ordering: int = 0

    # information about origin ------------------------------------------------
    # overrides group information
    registered_on: str = ''  # date of registration in form '2021-01-01'
    registered_by: str = ''  # uuid of user
    author: str = ''  # name of the author
    author_url: str = ''  # link to author's page or account
    origin_url: str = ''  # link to the page where this content was seen
    comment: str = ''  # optional description of the entity

    # identification info
    signature: str = ''  # encoded signature string
    signature_type: str = ''  # human-readable type, like 'md5'

    previous: str = ''
    next: str = ''

    # string with arbitrary names, that represent some logical structure
    # supposed to be used in ordering, like 'plants,flowers,daisy'
    hierarchy: str = ''

    # rights required to see this entity, extends original permissions
    permissions: FrozenSet[Permission] = field(default_factory=frozenset)

    # tags of the entity
    tags: FrozenSet[str] = field(default_factory=frozenset)
