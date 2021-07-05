# -*- coding: utf-8 -*-
"""Helper class that stores routes for entities.
"""
from typing import Dict

from omoide.core.hints import UUID

__all__ = [
    'Router',
]


class Router:
    """Helper class that stores routes for entities.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        self._memory: Dict[UUID, str] = {}

    def register_route(self, uuid: UUID, route: str) -> None:
        # FIXME
        self._memory[uuid] = route

    def get_route(self, uuid: UUID) -> str:
        # FIXME
        return self._memory[uuid]
