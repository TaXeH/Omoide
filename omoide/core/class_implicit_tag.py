# -*- coding: utf-8 -*-

"""Collection of hidden tags.
"""
from dataclasses import dataclass, field
from typing import FrozenSet, Iterator

from omoide.core.hints import UUID

__all__ = [
    'ImplicitTag',
]


# pylint: disable=R0902
@dataclass(frozen=True)
class ImplicitTag:
    """Collection of hidden tags.
    """
    uuid: UUID = ''  # unique synonym identifier, starts with i_
    theme_uuid: UUID = ''  # unique theme identifier, starts with t_
    # -------------------------------------------------------------------------
    description: str = ''  # human readable description of tag
    values: FrozenSet[str] = field(default_factory=frozenset)

    def __contains__(self, item: str) -> bool:
        """Return True if this tag is in out storage."""
        return item in self.values

    def __iter__(self) -> Iterator[str]:
        """Iterate on groups in the storage."""
        return iter(self.values)
