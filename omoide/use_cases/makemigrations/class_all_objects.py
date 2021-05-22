# -*- coding: utf-8 -*-

"""Helper type for data transfer.
"""
from dataclasses import dataclass
from typing import List

from omoide import core
from omoide.use_cases.makemigrations.class_relocation import Relocation


@dataclass
class AllObjects:
    """Helper type for data transfer.
    """
    realms: List[core.Realm]
    themes: List[core.Theme]
    groups: List[core.Group]
    implicit_tags: List[core.ImplicitTag]
    synonyms: List[core.Synonym]
    metas: List[core.Meta]
    # users FIXME
    relocations: List[Relocation]
