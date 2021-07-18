# -*- coding: utf-8 -*-
"""Helper type for a single file relocation/conversion.
"""
from dataclasses import dataclass

__all__ = [
    'Relocation',
]


@dataclass
class Relocation:
    """Helper type for a single file relocation/conversion.
    """
    uuid: str
    path_from: str
    path_to: str
    filename: str
    width: int
    height: int
    operation_type: str
