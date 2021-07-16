# -*- coding: utf-8 -*-

"""Collection of classes used on initial parsing stage.
"""
from typing import List

from pydantic import BaseModel, Field

__all__ = [
    'Source',
    'Realm',
    'Theme',
    'Synonym',
    'ImplicitTag',
    'Group',
    'User',
]


# TODO - add validators for uuid fields
# class UUIDCheckMixin(BaseModel):
#     """Mixin that checks UUID field."""
#     uuid: str
#
#     @validator('uuid')
#     def must_be_variable(self, value):
#         if not str(value).startswith(constants.VARIABLE_SIGN):
#             raise ValueError(
#                 f'UUIDS are accepted only as variables, not {value!r}'
#             )
#         return value


class Realm(BaseModel):
    """User defined Realm."""
    uuid: str
    route: str
    label: str
    tags: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)


class _NestedField(BaseModel):
    """Base class for nested elements of theme."""
    uuid: str
    theme_uuid: str
    label: str
    values: List[str] = Field(default_factory=list)


class Synonym(_NestedField):
    """User defined Synonym."""


class ImplicitTag(_NestedField):
    """User defined ImplicitTag."""


class Theme(BaseModel):
    """User defined Theme."""
    uuid: str
    realm_uuid: str
    route: str
    label: str
    synonyms: List[Synonym] = Field(default_factory=dict)
    implicit_tags: List[ImplicitTag] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)


class _BaseEntity(BaseModel):
    """Base class for Group and Meta."""
    registered_on: str = Field(default='')
    registered_by: str = Field(default='')
    author: str = Field(default='')
    author_url: str = Field(default='')
    origin_url: str = Field(default='')
    comment: str = Field(default='')
    hierarchy: str = Field(default='')
    tags: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)


class Group(_BaseEntity):
    """User defined Theme."""
    uuid: str
    theme_uuid: str
    route: str
    label: str


class Meta(_BaseEntity):
    """User defined Meta."""
    realm_uuid: str
    theme_uuid: str
    group_uuid: str
    filenames: List[str]


class User(BaseModel):
    """User defined User (lol)."""
    uuid: str
    name: str
    permissions: List[str] = Field(default_factory=list)
    # TODO - User must have more fields than that


class Source(BaseModel):
    """All source entries combined."""
    realms: List[Realm] = Field(default_factory=list)
    themes: List[Theme] = Field(default_factory=list)
    synonyms: List[Synonym] = Field(default_factory=list)
    implicit_tags: List[ImplicitTag] = Field(default_factory=list)
    groups: List[Group] = Field(default_factory=list)
    metas: List[Meta] = Field(default_factory=list)
    users: List[User] = Field(default_factory=list)
