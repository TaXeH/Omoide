# -*- coding: utf-8 -*-

"""Special class that handles UUID generation.
"""
import typing
import uuid as uuid_module
from collections import ChainMap
from typing import Set, Dict, Collection, Optional

from omoide.core import constants
from omoide.core.constants import VARIABLE_SIGN
from omoide.core.hints import UUID

__all__ = [
    'UUIDMaster',
]


class UUIDMaster:
    """Special class that handles UUID generation."""
    valid_prefixes = frozenset(constants.ALL_PREFIXES)

    def __init__(self,
                 aliases: Optional[Dict[str, str]] = None,
                 uuids_realms: Optional[Collection[str]] = None,
                 uuids_themes: Optional[Collection[str]] = None,
                 uuids_groups: Optional[Collection[str]] = None,
                 uuids_metas: Optional[Collection[str]] = None,
                 uuids_synonyms: Optional[Collection[str]] = None,
                 uuids_implicit_tags: Optional[Collection[str]] = None,
                 uuids_users: Optional[Collection[str]] = None,
                 ) -> None:
        """Initialize instance."""
        self.aliases: Dict[str, str] = aliases or {}

        def make_set(collection: Optional[Collection[str]]) -> Set[str]:
            """Shorthand for ternary operator."""
            if collection is None:
                return set()
            return set(collection)

        self.uuids_realms = make_set(uuids_realms)
        self.uuids_themes = make_set(uuids_themes)
        self.uuids_groups = make_set(uuids_groups)
        self.uuids_metas = make_set(uuids_metas)
        self.uuids_synonyms = make_set(uuids_synonyms)
        self.uuids_implicit_tags = make_set(uuids_implicit_tags)
        self.uuids_users = make_set(uuids_users)

        self._cached_r_uuids: Dict[str, str] = {}
        self._cached_t_uuids: Dict[str, str] = {}
        self._cached_g_uuids: Dict[str, str] = {}
        self._cached_m_uuids: Dict[str, str] = {}
        self._cached_s_uuids: Dict[str, str] = {}
        self._cached_i_uuids: Dict[str, str] = {}
        self._cached_u_uuids: Dict[str, str] = {}

        self.cache = ChainMap(self._cached_r_uuids,
                              self._cached_t_uuids,
                              self._cached_g_uuids,
                              self._cached_m_uuids,
                              self._cached_s_uuids,
                              self._cached_i_uuids,
                              self._cached_u_uuids)

        self._prefix_to_set = {
            constants.PREFIX_REALM: self.uuids_realms,
            constants.PREFIX_THEME: self.uuids_themes,
            constants.PREFIX_GROUP: self.uuids_groups,
            constants.PREFIX_META: self.uuids_metas,
            constants.PREFIX_SYNONYM: self.uuids_synonyms,
            constants.PREFIX_IMPL_TAG: self.uuids_implicit_tags,
            constants.PREFIX_USER: self.uuids_users,
        }

        self._prefix_to_cache = {
            constants.PREFIX_REALM: self._cached_r_uuids,
            constants.PREFIX_THEME: self._cached_t_uuids,
            constants.PREFIX_GROUP: self._cached_g_uuids,
            constants.PREFIX_META: self._cached_m_uuids,
            constants.PREFIX_SYNONYM: self._cached_s_uuids,
            constants.PREFIX_IMPL_TAG: self._cached_i_uuids,
            constants.PREFIX_USER: self._cached_u_uuids,
        }

        # avoiding collisions on aliases
        for key, alias in self.aliases.items():
            if key.startswith(VARIABLE_SIGN):
                raise NameError(
                    f'You should use alias names without {VARIABLE_SIGN}'
                )

            prefix = alias[0]

            if prefix not in self.valid_prefixes:
                raise NameError(
                    f'Wrong prefix {prefix!r}, allowed '
                    f'prefixes are: {constants.ALL_PREFIXES}'
                )
            storage_set = self.get_set_by_prefix(prefix)
            storage_set.add(alias)

    def __contains__(self, uuid: typing.Union[str, UUID]) -> bool:
        """Return True if this UUID is already used."""
        return any([
            uuid in self.uuids_realms,
            uuid in self.uuids_themes,
            uuid in self.uuids_groups,
            uuid in self.uuids_metas,
            uuid in self.uuids_synonyms,
            uuid in self.uuids_implicit_tags,
            uuid in self.uuids_users,
        ])

    @staticmethod
    def generate_uuid4() -> UUID:
        """Generate basic UUID4."""
        return UUID(str(uuid_module.uuid4()))

    def get_set_by_prefix(self, prefix: str) -> Set[str]:
        """Get storage set corresponding to prefix."""
        return self._prefix_to_set[prefix]

    def get_cache_by_prefix(self, prefix: str) -> Dict[str, str]:
        """Get cache corresponding to prefix."""
        return self._prefix_to_cache[prefix]

    @classmethod
    def split_variable_name(cls, variable: str) -> typing.Tuple[str, str]:
        """Convert identifier into pair of parameters."""
        prefix, number = variable.split('_')

        if prefix not in cls.valid_prefixes:
            raise NameError(
                f'Wrong prefix {prefix!r}, allowed '
                f'prefixes are: {constants.ALL_PREFIXES}'
            )

        return prefix, number

    def get_uuid_for_variable(self, variable: str) -> UUID:
        """Get or create UUID for given variable.

        For example '$r_1' -> 'r_e81efbc0-4ad4-4757-9d16-dd83e7765394'
        """
        if not variable.startswith(VARIABLE_SIGN):
            raise NameError(
                f'You should use variable names with leading {VARIABLE_SIGN}'
            )

        variable = variable.lstrip(constants.VARIABLE_SIGN)
        identifier = self.aliases.get(variable)

        if identifier is not None:
            return UUID(identifier)

        identifier = self.cache.get(variable)

        if identifier is not None:
            return UUID(identifier)

        prefix, _ = self.split_variable_name(variable)

        storage = self.get_set_by_prefix(prefix)
        cache = self.get_cache_by_prefix(prefix)

        identifier = self.generate_and_add_uuid(storage, prefix)
        cache[variable] = identifier

        return UUID(identifier)

    def generate_uuid(self,
                      existing_uuids: Set[str], prefix: str) -> UUID:
        """Create new UUID."""
        new_uuid = f'{prefix}_{self.generate_uuid4()}'
        while new_uuid in existing_uuids:
            new_uuid = f'{prefix}_{self.generate_uuid4()}'
        return UUID(new_uuid)

    def generate_and_add_uuid(self,
                              existing_uuids: Set[str], prefix: str) -> UUID:
        """Create and add new UUID."""
        new_uuid = self.generate_uuid(existing_uuids, prefix)
        existing_uuids.add(new_uuid)
        return UUID(new_uuid)

    def generate_uuid_meta(self) -> UUID:
        """Create and add new UUID for meta."""
        return self.generate_and_add_uuid(existing_uuids=self.uuids_metas,
                                          prefix=constants.PREFIX_META)

    def __add__(self, other) -> 'UUIDMaster':
        """Sum two UUID Masters."""
        cls = type(self)
        if not isinstance(other, cls):
            raise TypeError(
                f'{cls.__name__} can be added only to '
                'an instance of the same type'
            )

        return cls(
            aliases={**self.aliases, **other.aliases},
            uuids_realms=self.uuids_realms.union(other.uuids_realms),
            uuids_themes=self.uuids_themes.union(other.uuids_themes),
            uuids_groups=self.uuids_groups.union(other.uuids_groups),
            uuids_metas=self.uuids_metas.union(other.uuids_metas),
            uuids_synonyms=self.uuids_synonyms.union(other.uuids_synonyms),
            uuids_implicit_tags=self.uuids_implicit_tags.union(
                other.uuids_implicit_tags
            ),
            uuids_users=self.uuids_users.union(other.uuids_users),
        )

    def add_new_aliases(self, new_aliases: Dict[str, str]) -> None:
        """Add new aliases."""
        self.aliases.update(new_aliases)
