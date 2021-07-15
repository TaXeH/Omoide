# -*- coding: utf-8 -*-

"""Special class that handles UUID generation.
"""
import uuid as uuid_module
from typing import Set, Collection, Optional, List, Union, Sequence, Tuple

from omoide import constants
from omoide import core

__all__ = [
    'UUIDMaster',
]

RawValues = Optional[Sequence[core.RawUUID]]
Values = Optional[Collection[core.UUID]]


class UUIDMaster:
    """Special class that handles UUID generation."""

    def __init__(self,
                 uuids_queue: RawValues = None,
                 uuids_realms: Values = None,
                 uuids_themes: Values = None,
                 uuids_groups: Values = None,
                 uuids_metas: Values = None,
                 uuids_users: Values = None,
                 ) -> None:
        """Initialize instance."""

        def make_set(collection: Optional[Collection[core.UUID]]
                     ) -> Set[core.UUID]:
            """Shorthand for ternary operator."""
            if collection is None:
                return set()
            return set(collection)

        self.uuids_realms = make_set(uuids_realms)
        self.uuids_themes = make_set(uuids_themes)
        self.uuids_groups = make_set(uuids_groups)
        self.uuids_metas = make_set(uuids_metas)
        self.uuids_users = make_set(uuids_users)

        uuids_queue = uuids_queue or []

        self.given_queue: List[core.RawUUID] = list(reversed(uuids_queue))
        self.used_queue: List[core.RawUUID] = []

    def __contains__(self, uuid: Union[str, core.UUID]) -> bool:
        """Return True if this UUID is already used."""
        return any([
            uuid in self.uuids_realms,
            uuid in self.uuids_themes,
            uuid in self.uuids_groups,
            uuid in self.uuids_metas,
            uuid in self.uuids_users,
        ])

    @staticmethod
    def generate_uuid4() -> core.RawUUID:
        """Generate basic UUID4."""
        return core.RawUUID(str(uuid_module.uuid4()))

    def generate_uuid(self, existing_uuids: Set[core.UUID],
                      prefix: str) -> Tuple[core.UUID, core.RawUUID]:
        """Create new UUID."""
        original = self.generate_uuid4()
        new_uuid = f'{prefix}_{original}'
        while new_uuid in existing_uuids:
            original = self.generate_uuid4()
            new_uuid = f'{prefix}_{original}'
        return core.UUID(new_uuid), original

    def generate_and_add_uuid(self, existing_uuids: Set[core.UUID],
                              prefix: str) -> core.UUID:
        """Create and add new UUID."""
        if self.given_queue:
            original = self.given_queue.pop()
            new_uuid = f'{prefix}_{original}'
        else:
            new_uuid, original = self.generate_uuid(existing_uuids, prefix)

        self.used_queue.append(original)
        existing_uuids.add(new_uuid)
        return core.UUID(new_uuid)

    def generate_uuid_realm(self) -> core.UUID:
        """Create and add new UUID for realm."""
        return self.generate_and_add_uuid(existing_uuids=self.uuids_realms,
                                          prefix=constants.PREFIX_REALM)

    def generate_uuid_theme(self) -> core.UUID:
        """Create and add new UUID for theme."""
        return self.generate_and_add_uuid(existing_uuids=self.uuids_themes,
                                          prefix=constants.PREFIX_THEME)

    def generate_uuid_group(self) -> core.UUID:
        """Create and add new UUID for group."""
        return self.generate_and_add_uuid(existing_uuids=self.uuids_groups,
                                          prefix=constants.PREFIX_GROUP)

    def generate_uuid_meta(self) -> core.UUID:
        """Create and add new UUID for meta."""
        return self.generate_and_add_uuid(existing_uuids=self.uuids_metas,
                                          prefix=constants.PREFIX_META)

    def generate_uuid_user(self) -> core.UUID:
        """Create and add new UUID for user."""
        return self.generate_and_add_uuid(existing_uuids=self.uuids_users,
                                          prefix=constants.PREFIX_USER)

    def insert_queue(self, uuids: Sequence[core.RawUUID]) -> None:
        """Add uuids queue."""
        self.given_queue = list(reversed(uuids)) + self.given_queue

    def __add__(self, other) -> 'UUIDMaster':
        """Sum two UUID Masters."""
        cls = type(self)
        if not isinstance(other, cls):
            raise TypeError(
                f'{cls.__name__} can be added only to '
                'an instance of the same type'
            )

        if any([self.given_queue,
                self.used_queue,
                other.given_queue,
                other.used_queue]):
            raise ValueError(
                'You must empty queues before adding uuid masters'
            )

        return cls(
            uuids_realms=self.uuids_realms.union(other.uuids_realms),
            uuids_themes=self.uuids_themes.union(other.uuids_themes),
            uuids_groups=self.uuids_groups.union(other.uuids_groups),
            uuids_metas=self.uuids_metas.union(other.uuids_metas),
            uuids_users=self.uuids_users.union(other.uuids_users),
        )

    def extract_queue(self) -> List[core.RawUUID]:
        """Get all generated UUIDS."""
        return self.used_queue.copy()

    def clear_queue(self):
        """Clear list of generated UUIDS."""
        self.used_queue.clear()
