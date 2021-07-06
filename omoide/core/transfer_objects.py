# -*- coding: utf-8 -*-

"""Primitive types used to transfer information between modules.
"""
from dataclasses import dataclass
from typing import Optional

__all__ = [
    'Relocation',
    'SQL',
]


@dataclass
class Relocation:
    """Helper type for a single file relocation/conversion.
    """
    uuid: str
    path_from: str
    path_to: str
    width: int
    height: int
    operation_type: str


class SQL:
    """Helper type for a single SQL command representation.
    """

    def __init__(self, statement):
        """Initialize instance."""
        self.statement = statement
        self._cached_statement: Optional[str] = None

    def __str__(self) -> str:
        """Return textual representation."""
        if self._cached_statement is None:
            stmt = self.statement.compile(
                compile_kwargs={"literal_binds": True}
            )
            self._cached_statement = str(stmt)
        return self._cached_statement
