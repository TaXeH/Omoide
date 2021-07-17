# -*- coding: utf-8 -*-
"""Helper class that is created to work with variables in source files.
"""
from collections import ChainMap
from functools import partial
from typing import Dict

from omoide import constants
from omoide.core.hints import UUID
from omoide.use_cases.unite.class_uuid_master import UUIDMaster

__all__ = [
    'IdentityMaster',
]


class IdentityMaster:
    """Helper class that is created to work with variables in source files."""

    def __init__(self) -> None:
        """Initialize instance."""
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

        self._prefix_to_method = {
            constants.PREFIX_REALM: 'generate_uuid_realm',
            constants.PREFIX_THEME: 'generate_uuid_theme',
            constants.PREFIX_SYNONYM: 'generate_uuid_synonym',
            constants.PREFIX_IMPLICIT_TAG: 'generate_uuid_implicit_tag',
            constants.PREFIX_GROUP: 'generate_uuid_group',
            constants.PREFIX_META: 'generate_uuid_meta',
            constants.PREFIX_USER: 'generate_uuid_user',
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

        cache = self._prefix_to_cache[prefix]
        uuid = cache.get(variable)

        if uuid is None:
            if strict:
                raise KeyError(
                    f'Variable {variable} in not found '
                    f'in cache by prefix {prefix}'
                )

            generator = getattr(uuid_master, self._prefix_to_method[prefix])
            uuid = generator()
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

    def extract(self, branch: str, leaf: str) -> Dict[str, Dict[str, str]]:
        """Serialize to a dictionary.

        Note that we're avoiding adding static data here.
        """
        selector = partial(self.select_by_branch, branch, leaf)
        return {
            'realms': selector(self._cached_r_uuids),
            'themes': selector(self._cached_t_uuids),
            'synonyms': selector(self._cached_s_uuids),
            'implicit_tags': selector(self._cached_i_uuids),
            'groups': selector(self._cached_g_uuids),
            'metas': selector(self._cached_m_uuids),
            'users': selector(self._cached_u_uuids),
        }

    @staticmethod
    def select_by_branch(branch: str, leaf: str,
                         storage: Dict[str, str]) -> Dict[str, str]:
        """Select only variables of given branch/leaf"""
        return {
            variable: value
            for variable, value in storage.items()
            if variable.startswith(f'{constants.VARIABLE_SIGN}{branch}.{leaf}')
        }

    def add_variable(self, variable: str, value: str) -> None:
        """Add external variable to the storage."""
        prefix = self.get_prefix(variable)

        if prefix not in constants.ALL_PREFIXES_SET:
            raise ValueError(
                f'Unknown prefix {prefix!r} for variable {variable}'
            )

        if value.startswith(constants.VARIABLE_SIGN):
            raise ValueError(
                f'Variable {variable} should '
                f'contain actual value, not {value}'
            )

        cache = self._prefix_to_cache[prefix]
        cache[variable] = UUID(value)
