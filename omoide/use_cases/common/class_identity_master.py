# -*- coding: utf-8 -*-
"""Helper class that is created to work with variables in source files.
"""
from collections import ChainMap
from typing import Dict

from omoide import constants
from omoide.core.hints import UUID
from omoide.use_cases.common.class_uuid_master import UUIDMaster

__all__ = [
    'IdentityMaster',
]


class IdentityMaster:
    """Helper class that is created to work with variables in source files."""

    def __init__(self) -> None:
        """Initialize instance."""
        self._static_cached_r_uuids: Dict[str, UUID] = {}
        self._static_cached_t_uuids: Dict[str, UUID] = {}
        self._static_cached_s_uuids: Dict[str, UUID] = {}
        self._static_cached_i_uuids: Dict[str, UUID] = {}
        self._static_cached_g_uuids: Dict[str, UUID] = {}
        self._static_cached_m_uuids: Dict[str, UUID] = {}
        self._static_cached_u_uuids: Dict[str, UUID] = {}

        self._static_cache = ChainMap(
            self._static_cached_r_uuids,
            self._static_cached_t_uuids,
            self._static_cached_s_uuids,
            self._static_cached_i_uuids,
            self._static_cached_g_uuids,
            self._static_cached_m_uuids,
            self._static_cached_u_uuids,
        )

        self._prefix_to_static_cache = {
            constants.PREFIX_REALM: self._static_cached_r_uuids,
            constants.PREFIX_THEME: self._static_cached_t_uuids,
            constants.PREFIX_SYNONYM: self._static_cached_s_uuids,
            constants.PREFIX_IMPLICIT_TAG: self._static_cached_i_uuids,
            constants.PREFIX_GROUP: self._static_cached_g_uuids,
            constants.PREFIX_META: self._static_cached_m_uuids,
            constants.PREFIX_USER: self._static_cached_u_uuids,
        }

        self._cached_r_uuids: Dict[str, UUID] = {}
        self._cached_t_uuids: Dict[str, UUID] = {}
        self._cached_s_uuids: Dict[str, UUID] = {}
        self._cached_i_uuids: Dict[str, UUID] = {}
        self._cached_g_uuids: Dict[str, UUID] = {}
        self._cached_m_uuids: Dict[str, UUID] = {}
        self._cached_u_uuids: Dict[str, UUID] = {}

        self._cache = ChainMap(
            self._cached_r_uuids,
            self._cached_t_uuids,
            self._cached_s_uuids,
            self._cached_i_uuids,
            self._cached_g_uuids,
            self._cached_m_uuids,
            self._cached_u_uuids,
        )

        self._prefix_to_cache = {
            constants.PREFIX_REALM: self._cached_r_uuids,
            constants.PREFIX_THEME: self._cached_t_uuids,
            constants.PREFIX_SYNONYM: self._cached_s_uuids,
            constants.PREFIX_IMPLICIT_TAG: self._cached_i_uuids,
            constants.PREFIX_GROUP: self._cached_g_uuids,
            constants.PREFIX_META: self._cached_m_uuids,
            constants.PREFIX_USER: self._cached_u_uuids,
        }

    @staticmethod
    def get_prefix(string: str) -> str:
        """Return prefix of the variable."""
        elements = string.split('.')
        variable = elements[-1].lstrip(constants.VARIABLE_SIGN)
        return variable[0]

    def get_uuid_generic(self, variable: str, uuid_master: UUIDMaster,
                         supposed_prefix: str, strict: bool = False) -> UUID:
        """Common method for uuid extraction."""
        prefix = self.get_prefix(variable)

        if prefix not in constants.ALL_PREFIXES_SET:
            raise ValueError(
                f'Unknown prefix {prefix!r} for variable {variable}'
            )

        if prefix != supposed_prefix:
            raise ValueError(
                f'Variable {variable} does not '
                f'conform prefix {supposed_prefix}'
            )

        static_cache = self._prefix_to_static_cache[prefix]

        if variable in static_cache:
            return static_cache[variable]

        cache = self._prefix_to_cache[prefix]
        uuid = cache.get(variable)

        if uuid is None:
            if strict:
                raise KeyError(
                    f'Variable {variable} in not found '
                    f'in cache by prefix {prefix}'
                )
            uuid = uuid_master.generate_uuid_realm()
            cache[variable] = uuid
        return uuid

    def get_realm_uuid(self, variable: str, uuid_master: UUIDMaster,
                       strict: bool = False) -> UUID:
        """Get UUID from variable."""
        return self.get_uuid_generic(variable, uuid_master,
                                     constants.PREFIX_REALM, strict)

    def get_theme_uuid(self, variable: str, uuid_master: UUIDMaster,
                       strict: bool = False) -> UUID:
        """Get UUID from variable."""
        return self.get_uuid_generic(variable, uuid_master,
                                     constants.PREFIX_THEME, strict)

    def get_synonym_uuid(self, variable: str, uuid_master: UUIDMaster,
                         strict: bool = False) -> UUID:
        """Get UUID from variable."""
        return self.get_uuid_generic(variable, uuid_master,
                                     constants.PREFIX_SYNONYM, strict)

    def get_implicit_tag_uuid(self, variable: str, uuid_master: UUIDMaster,
                              strict: bool = False) -> UUID:
        """Get UUID from variable."""
        return self.get_uuid_generic(variable, uuid_master,
                                     constants.PREFIX_IMPLICIT_TAG, strict)

    def get_group_uuid(self, variable: str, uuid_master: UUIDMaster,
                       strict: bool = False) -> UUID:
        """Get UUID from variable."""
        return self.get_uuid_generic(variable, uuid_master,
                                     constants.PREFIX_GROUP, strict)

    def get_user_uuid(self, variable: str, uuid_master: UUIDMaster,
                      strict: bool = False) -> UUID:
        """Get UUID from variable."""
        return self.get_uuid_generic(variable, uuid_master,
                                     constants.PREFIX_USER, strict)

    def freeze(self) -> None:
        """Move all new variables into static sections."""
        self._static_cached_r_uuids.update(self._cached_r_uuids)
        self._static_cached_t_uuids.update(self._cached_t_uuids)
        self._static_cached_s_uuids.update(self._cached_s_uuids)
        self._static_cached_i_uuids.update(self._cached_i_uuids)
        self._static_cached_g_uuids.update(self._cached_g_uuids)
        self._static_cached_m_uuids.update(self._cached_m_uuids)
        self._static_cached_u_uuids.update(self._cached_u_uuids)

        self._cached_r_uuids.clear()
        self._cached_t_uuids.clear()
        self._cached_s_uuids.clear()
        self._cached_i_uuids.clear()
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
            'synonyms': self._cached_s_uuids.copy(),
            'implicit_tags': self._cached_i_uuids.copy(),
            'groups': self._cached_g_uuids.copy(),
            'metas': self._cached_m_uuids.copy(),
            'users': self._cached_u_uuids.copy(),
        }
