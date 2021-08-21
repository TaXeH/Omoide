# -*- coding: utf-8 -*-

"""Statistics on current level of display.
"""
from collections import defaultdict
from typing import (
    List, Dict, Collection, Generator, Tuple, Union, Any, Optional
)

from omoide import utils

__all__ = [
    'Statistics',
]


class Statistics:
    """Statistics on current level of display.
    """

    def __init__(self, min_date: str = '', max_date: str = '',
                 total_items: int = 0, total_size: int = 0,
                 tags: Optional[List[str]] = None) -> None:
        """Initialize instance."""
        self.min_date = min_date
        self.max_date = max_date
        self.total_items = total_items
        self.total_size = total_size
        self._tags: List[str] = tags or []
        self._tags_by_freq: List[Tuple[str, int]] = []
        self._tags_by_alphabet: List[Tuple[str, List[str]]] = []
        self._need_recalculation = True

    def __len__(self) -> int:
        """Return total amount of tags."""
        return len(self._tags)

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'<{type(self).__name__}, n={self.total_items}>'

    def __iter__(self) -> Generator[Tuple[str, Union[int, str]], None, None]:
        """Iterate on pais of parameters, but not nested ones."""
        for key, value in self.as_dict().items():
            if isinstance(value, (int, str)):
                yield key, value

    def __add__(self, other) -> 'Statistics':
        """Sum two statistics together."""
        cls = type(self)

        if not isinstance(other, cls):
            return NotImplemented

        instance = cls()
        instance.min_date = min(self.min_date or other.min_date,
                                other.min_date or self.min_date)
        instance.max_date = max(self.max_date or other.max_date,
                                other.max_date or self.max_date)
        instance.total_items = self.total_items + other.total_items
        instance.total_size = self.total_size + other.total_size
        instance.tags = self.tags + other.tags
        return instance

    def add(self, item_date: str, item_size: int,
            item_tags: Collection[str]) -> None:
        """Add information about single item."""
        self.total_items += 1
        self.total_size += item_size
        self.min_date = min(self.min_date or item_date, item_date)
        self.max_date = max(self.max_date or item_date, item_date)
        self._tags.extend(item_tags)
        self._need_recalculation = True

    def as_dict(self) -> Dict[str, Any]:
        """Return statistics as a dictionary."""
        return {
            'total_items': self.total_items,
            'total_size': self.total_size,
            'min_date': self.min_date,
            'max_date': self.max_date,
            'tags': self.tags,
        }

    @classmethod
    def from_dict(cls, source: Dict[str, Any]) -> 'Statistics':
        """Create instance from dictionary."""
        return cls(
            min_date=source['min_date'],
            max_date=source['max_date'],
            total_items=source['total_items'],
            total_size=source['total_size'],
            tags=source['tags'],
        )

    def _recalculate(self) -> None:
        """Update inner storages."""
        # frequency -----------------------------------------------------------
        tags_stats = defaultdict(int)
        for tag in self._tags:
            tags_stats[tag] += 1

        self._tags_by_freq = list(tags_stats.items())

        # by alphabet
        self._tags_by_freq.sort(key=lambda x: x[0], reverse=False)

        # by frequency
        self._tags_by_freq.sort(key=lambda x: x[1], reverse=True)

        # alphabet ------------------------------------------------------------
        self._tags_by_alphabet = list(
            utils.arrange_by_alphabet(self._tags).items()
        )

        self._need_recalculation = False

    @property
    def tags_by_frequency(self) -> List[Tuple[str, int]]:
        """Return list of tags sorted by popularity.

        Example:
        [
            ("tag_1", 25),
            ("tag_2", 14),
        ]
        """
        if self._need_recalculation:
            self._recalculate()
        return self._tags_by_freq

    @property
    def tags_by_alphabet(self) -> List[Tuple[str, List[str]]]:
        """Return map of tags by alphabet.

        Example:
        [
            ("A", ["aqua", "azure"]),
            ("B"", ["bobcat"]),
        ]
        """
        if self._need_recalculation:
            self._recalculate()
        return self._tags_by_alphabet

    @property
    def tags(self) -> List[str]:
        """Return copy of inner tags."""
        return self._tags.copy()

    @tags.setter
    def tags(self, new_tags: Collection[str]) -> None:
        """Assign new tags."""
        self._tags = self._tags + list(new_tags)
        self._need_recalculation = True
