# -*- coding: utf-8 -*-

"""Helper type for a single file relocation/conversion.
"""
from dataclasses import dataclass


@dataclass
class Relocation:
    """Helper type for a single file relocation/conversion.
    """
    uuid: str
    realm_uuid: str
    theme_uuid: str
    group_uuid: str
    source_path: str
    width: int
    height: int
    operation_type: str
