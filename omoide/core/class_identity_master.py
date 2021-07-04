# -*- coding: utf-8 -*-
"""Helper class that is created to work with variables in source files.
"""
from collections import ChainMap
from typing import Dict

from omoide.core import constants
from omoide.core.class_uuid_master import UUIDMaster
from omoide.core.hints import UUID

__all__ = [
    'IdentityMaster',
]


class IdentityMaster:
    """Helper class that is created to work with variables in source files."""

    def __init__(self) -> None:
        """Initialize instance."""
        self._cached_r_uuids: Dict[str, UUID] = {}
        self._cached_t_uuids: Dict[str, UUID] = {}
        self._cached_g_uuids: Dict[str, UUID] = {}
        self._cached_m_uuids: Dict[str, UUID] = {}
        self._cached_u_uuids: Dict[str, UUID] = {}

        self._cache = ChainMap(self._cached_r_uuids,
                               self._cached_t_uuids,
                               self._cached_g_uuids,
                               self._cached_m_uuids,
                               self._cached_u_uuids)

        self._prefix_to_cache = {constants.PREFIX_REALM: self._cached_r_uuids,
                                 constants.PREFIX_THEME: self._cached_t_uuids,
                                 constants.PREFIX_GROUP: self._cached_g_uuids,
                                 constants.PREFIX_META: self._cached_m_uuids,
                                 constants.PREFIX_USER: self._cached_u_uuids}

    def get_realm_uuid(self, variable: str, uuid_master: UUIDMaster) -> UUID:
        """Get UUID from variable."""
        # FIXME - remove duplication
        uuid = self._cached_r_uuids.get(variable)
        if uuid is None:
            uuid = uuid_master.generate_uuid_realm()
            self._cached_r_uuids[variable] = uuid
        return uuid

    def get_theme_uuid(self, variable: str, uuid_master: UUIDMaster) -> UUID:
        """Get UUID from variable."""
        # FIXME - remove duplication
        uuid = self._cached_t_uuids.get(variable)
        if uuid is None:
            uuid = uuid_master.generate_uuid_theme()
            self._cached_t_uuids[variable] = uuid
        return uuid

    def get_group_uuid(self, variable: str, uuid_master: UUIDMaster) -> UUID:
        """Get UUID from variable."""
        # FIXME - remove duplication
        uuid = self._cached_g_uuids.get(variable)
        if uuid is None:
            uuid = uuid_master.generate_uuid_group()
            self._cached_g_uuids[variable] = uuid
        return uuid

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """Serialize to a dictionary."""
        return {
            'realms': self._cached_r_uuids,
            'themes': self._cached_t_uuids,
            'groups': self._cached_g_uuids,
            'metas': self._cached_m_uuids,
            'users': self._cached_u_uuids,
        }
