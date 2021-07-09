# -*- coding: utf-8 -*-

"""Tools that should return same results during migration/relocation/etc.
"""
import random
import string
from datetime import datetime
from functools import lru_cache

from omoide import constants

__all__ = [
    'get_now',
    'get_today',
    'get_revision_number',
]


@lru_cache()
def get_today() -> str:
    """Get today date as a string."""
    return str(datetime.now().date())


@lru_cache()
def get_now() -> str:
    """Get current moment as a string.

    Note that we're using only one moment
    for all operations through all migration creation.
    """
    return str(datetime.now().replace(microsecond=0))


@lru_cache()
def get_revision_number(length: int = constants.REVISION_LEN) -> str:
    """Generate unique revision number from os random generator."""
    symbols = string.ascii_lowercase + string.digits
    tokens = [random.choice(symbols) for _ in range(length)]
    return ''.join(tokens)
