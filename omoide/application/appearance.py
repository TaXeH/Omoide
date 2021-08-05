# -*- coding: utf-8 -*-
"""Styling things.
"""

from omoide import utils


def get_note_on_search(total: int, duration: float) -> str:
    """Return description of search duration."""
    _total = utils.sep_digits(total)
    _duration = '{:0.4f}'.format(duration)

    note = f'Found {_total} records in {_duration} seconds'

    return note
