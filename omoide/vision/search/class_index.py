# -*- coding: utf-8 -*-

"""Fast search storage.
"""
from collections import defaultdict
from typing import Set


class IndexItem:
    """Typical metarecord."""
    __slots__ = ('uuid', 'payload')

    def __init__(self, uuid: str, payload: str = '') -> None:
        """Initialize instance."""
        self.uuid = uuid
        self.payload = payload

    def __eq__(self, other) -> bool:
        """Return True if object has same uuid."""
        return self.uuid == getattr(other, 'uuid', None)

    def __hash__(self) -> int:
        """Return hash of the uuid."""
        return hash(self.uuid)


class Index:
    """Fast search storage.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self.storage = defaultdict(set)

    def add(self, key: str, item: IndexItem) -> None:
        """Put item into index."""
        self.storage[key].add(item)

    def get(self, key: str) -> Set[IndexItem]:
        """Get set of items from the storage."""
        return self.storage.get(key, set())
