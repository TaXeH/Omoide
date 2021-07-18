# -*- coding: utf-8 -*-
"""Helper class that stores routes for entities.
"""
from typing import Dict

__all__ = [
    'Router',
]


class Router:
    """Helper class that stores routes for entities.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._memory: Dict[str, str] = {}

    def register_route(self, uuid: str, route: str) -> None:
        # FIXME
        self._memory[uuid] = route

    def get_route(self, uuid: str) -> str:
        # FIXME
        return self._memory[uuid]
