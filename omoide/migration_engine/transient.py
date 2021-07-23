# -*- coding: utf-8 -*-

"""Collection of classes used after initial parsing is complete.
"""
from typing import List

from pydantic import BaseModel, Field, validator

from omoide import constants

__all__ = [
    'Realm',
    'Theme',
    'Group',
    'Meta',
    'User',
    'TagRealm',
    'TagTheme',
    'TagGroup',
    'TagMeta',
    'PermissionRealm',
    'PermissionTheme',
    'PermissionGroup',
    'PermissionMeta',
    'PermissionUser',
    'Synonym',
    'SynonymValue',
    'ImplicitTag',
    'ImplicitTagValue',
    'Unit',
]


class _CheckRealmUUIDMixin:
    """Additional checker."""

    @validator('uuid')
    def must_be_actual_realm_uuid(self, value):
        """Ensure that UUID is converted from variable."""
        assert not value.startswith(constants.VARIABLE_SIGN)
        assert value.startswith(constants.PREFIX_REALM)
        return value


class BaseUnitElement(BaseModel):
    """Base class for all parsed elements."""
    revision: str
    last_update: str


class Realm(BaseUnitElement, _CheckRealmUUIDMixin):
    """User defined Realm."""
    uuid: str
    route: str
    label: str


class Theme(BaseUnitElement):
    """User defined Theme."""
    uuid: str
    realm_uuid: str
    route: str
    label: str


class _BaseEntity(BaseUnitElement):
    """Base class for Group and Meta."""
    registered_on: str = Field(default='')
    registered_by: str = Field(default='')
    author: str = Field(default='')
    author_url: str = Field(default='')
    origin_url: str = Field(default='')
    comment: str = Field(default='')
    hierarchy: str = Field(default='')


class Group(_BaseEntity):
    """User defined Theme."""
    uuid: str
    theme_uuid: str
    route: str
    label: str


class Meta(_BaseEntity):
    """User defined Meta."""
    uuid: str
    realm_uuid: str
    theme_uuid: str
    group_uuid: str

    path_to_content: str = Field(default='')
    path_to_preview: str = Field(default='')
    path_to_thumbnail: str = Field(default='')
    original_filename: str = Field(default='')
    original_extension: str = Field(default='')
    width: int = Field(default=0)
    height: int = Field(default=0)
    resolution: float = Field(default=0.0)
    size: int = Field(default=0)
    duration: int = Field(default=0)
    type: str = Field(default='')
    ordering: int = Field(default=0)
    signature: str = Field(default='')
    signature_type: str = Field(default='')
    previous: str = Field(default='')
    next: str = Field(default='')


class User(BaseUnitElement):
    """User defined User (lol)."""
    uuid: str
    name: str
    # TODO - User must have more fields than that


class TagRealm(BaseUnitElement):
    realm_uuid: str
    value: str


class TagTheme(BaseUnitElement):
    theme_uuid: str
    value: str


class TagGroup(BaseUnitElement):
    group_uuid: str
    value: str


class TagMeta(BaseUnitElement):
    meta_uuid: str
    value: str


class PermissionRealm(BaseUnitElement):
    realm_uuid: str
    value: str


class PermissionTheme(BaseUnitElement):
    theme_uuid: str
    value: str


class PermissionGroup(BaseUnitElement):
    group_uuid: str
    value: str


class PermissionMeta(BaseUnitElement):
    meta_uuid: str
    value: str


class PermissionUser(BaseUnitElement):
    user_uuid: str
    value: str


class _NestedField(BaseUnitElement):
    """Base class for nested elements of theme."""
    uuid: str
    theme_uuid: str
    label: str


class Synonym(_NestedField):
    """User defined Synonym."""


class ImplicitTag(_NestedField):
    """User defined ImplicitTag."""


class SynonymValue(BaseUnitElement):
    """User defined Synonym."""
    synonym_uuid: str
    value: str


class ImplicitTagValue(BaseUnitElement):
    """User defined ImplicitTag."""
    implicit_tag_uuid: str
    value: str


class Unit(BaseModel):
    """All parsed entries combined."""
    realms: List[Realm] = Field(default_factory=list)
    themes: List[Theme] = Field(default_factory=list)
    groups: List[Group] = Field(default_factory=list)
    metas: List[Meta] = Field(default_factory=list)
    users: List[User] = Field(default_factory=list)

    tags_realms: List[TagRealm] = Field(default_factory=list)
    tags_themes: List[TagTheme] = Field(default_factory=list)
    tags_groups: List[TagGroup] = Field(default_factory=list)
    tags_metas: List[TagMeta] = Field(default_factory=list)

    synonyms: List[Synonym] = Field(default_factory=list)
    synonyms_values: List[SynonymValue] = Field(default_factory=list)

    implicit_tags: List[ImplicitTag] = Field(default_factory=list)
    implicit_tags_values: List[ImplicitTagValue] = Field(default_factory=list)

    permissions_realm: List[PermissionRealm] = Field(default_factory=list)
    permissions_themes: List[PermissionTheme] = Field(default_factory=list)
    permissions_groups: List[PermissionGroup] = Field(default_factory=list)
    permissions_metas: List[PermissionMeta] = Field(default_factory=list)
    permissions_users: List[PermissionUser] = Field(default_factory=list)
