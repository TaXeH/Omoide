# -*- coding: utf-8 -*-

"""Collection of search aliases.
"""
from dataclasses import dataclass, field
from typing import FrozenSet, Iterator

from omoide.core.hints import UUID

__all__ = [
    'Synonym',
]


# pylint: disable=R0902
@dataclass
class Synonym:
    """Collection of search aliases.
    """
    uuid: UUID = ''  # unique synonym identifier, starts with s_
    theme_uuid: UUID = ''  # unique theme identifier, starts with t_
    # -------------------------------------------------------------------------
    description: str = ''  # human readable description of alias
    values: FrozenSet[str] = field(default_factory=frozenset)

    def __contains__(self, item: str) -> bool:
        """Return True if this tag is in out storage."""
        return item in self.values

    def __iter__(self) -> Iterator[str]:
        """Iterate on groups in the storage."""
        return iter(self.values)
