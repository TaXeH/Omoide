# -*- coding: utf-8 -*-
"""Helper class that is created to work with variables in source files.
"""
from collections import ChainMap
from typing import Dict

from omoide import constants
from omoide.use_cases.common.class_uuid_master import UUIDMaster
from omoide.core.hints import UUID

__all__ = [
    'IdentityMaster',
]


class IdentityMaster:
    """Helper class that is created to work with variables in source files."""

    def __init__(self) -> None:
        """Initialize instance."""
        self._static_cached_r_uuids: Dict[str, UUID] = {}
        self._static_cached_t_uuids: Dict[str, UUID] = {}
        self._static_cached_g_uuids: Dict[str, UUID] = {}
        self._static_cached_m_uuids: Dict[str, UUID] = {}
        self._static_cached_u_uuids: Dict[str, UUID] = {}

        self._static_cache = ChainMap(
            self._static_cached_r_uuids,
            self._static_cached_t_uuids,
            self._static_cached_g_uuids,
            self._static_cached_m_uuids,
            self._static_cached_u_uuids,
        )

        self._prefix_to_static_cache = {
            constants.PREFIX_REALM: self._static_cached_r_uuids,
            constants.PREFIX_THEME: self._static_cached_t_uuids,
            constants.PREFIX_GROUP: self._static_cached_g_uuids,
            constants.PREFIX_META: self._static_cached_m_uuids,
            constants.PREFIX_USER: self._static_cached_u_uuids,
        }

        self._cached_r_uuids: Dict[str, UUID] = {}
        self._cached_t_uuids: Dict[str, UUID] = {}
        self._cached_g_uuids: Dict[str, UUID] = {}
        self._cached_m_uuids: Dict[str, UUID] = {}
        self._cached_u_uuids: Dict[str, UUID] = {}

        self._cache = ChainMap(
            self._cached_r_uuids,
            self._cached_t_uuids,
            self._cached_g_uuids,
            self._cached_m_uuids,
            self._cached_u_uuids,
        )

        self._prefix_to_cache = {
            constants.PREFIX_REALM: self._cached_r_uuids,
            constants.PREFIX_THEME: self._cached_t_uuids,
            constants.PREFIX_GROUP: self._cached_g_uuids,
            constants.PREFIX_META: self._cached_m_uuids,
            constants.PREFIX_USER: self._cached_u_uuids,
        }

    def get_realm_uuid(self, variable: str, uuid_master: UUIDMaster,
                       strict: bool = False) -> UUID:
        """Get UUID from variable."""
        # FIXME - remove duplication
        if variable in self._static_cached_r_uuids:
            return self._static_cached_r_uuids[variable]

        uuid = self._cached_r_uuids.get(variable)

        if uuid is None:
            if strict:
                raise KeyError
            uuid = uuid_master.generate_uuid_realm()
            self._cached_r_uuids[variable] = uuid
        return uuid

    def get_theme_uuid(self, variable: str, uuid_master: UUIDMaster,
                       strict: bool = False) -> UUID:
        """Get UUID from variable."""
        # FIXME - remove duplication
        if variable in self._static_cached_t_uuids:
            return self._static_cached_t_uuids[variable]

        uuid = self._cached_t_uuids.get(variable)

        if uuid is None:
            if strict:
                raise KeyError
            uuid = uuid_master.generate_uuid_theme()
            self._cached_t_uuids[variable] = uuid
        return uuid

    def get_group_uuid(self, variable: str, uuid_master: UUIDMaster,
                       strict: bool = False) -> UUID:
        """Get UUID from variable."""
        # FIXME - remove duplication
        if variable in self._static_cached_g_uuids:
            return self._static_cached_g_uuids[variable]

        uuid = self._cached_g_uuids.get(variable)

        if uuid is None:
            if strict:
                raise KeyError
            uuid = uuid_master.generate_uuid_group()
            self._cached_g_uuids[variable] = uuid
        return uuid

    def freeze(self) -> None:
        """Move all new variables into static sections."""
        self._static_cached_r_uuids.update(self._cached_r_uuids)
        self._static_cached_t_uuids.update(self._cached_t_uuids)
        self._static_cached_g_uuids.update(self._cached_g_uuids)
        self._static_cached_m_uuids.update(self._cached_m_uuids)
        self._static_cached_u_uuids.update(self._cached_u_uuids)

        self._cached_r_uuids.clear()
        self._cached_t_uuids.clear()
        self._cached_g_uuids.clear()
        self._cached_m_uuids.clear()
        self._cached_u_uuids.clear()

    def extract(self) -> Dict[str, Dict[str, str]]:
        """Serialize to a dictionary.

        Note that we're avoiding adding static data here.
        """
        return {
            'realms': self._cached_r_uuids.copy(),
            'themes': self._cached_t_uuids.copy(),
            'groups': self._cached_g_uuids.copy(),
            'metas': self._cached_m_uuids.copy(),
            'users': self._cached_u_uuids.copy(),
        }
