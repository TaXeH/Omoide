# -*- coding: utf-8 -*-

"""Helper type for a single file relocation/conversion.
"""
from dataclasses import dataclass


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

    def as_json(self):
        return {
            'uuid': self.uuid,
            'path_from': self.path_from,
            'path_to': self.path_to,
            'width': self.width,
            'height': self.height,
            'operation_type': self.operation_type,
        }