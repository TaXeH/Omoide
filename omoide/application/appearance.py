# -*- coding: utf-8 -*-
"""Styling things.
"""
from typing import Optional, List

from omoide import utils, constants


def get_note_on_search(total: int, duration: float) -> str:
    """Return description of search duration."""
    _total = utils.sep_digits(total)
    _duration = '{:0.4f}'.format(duration)

    note = f'Found {_total} records in {_duration} seconds'

    return note


def extract_active_themes(raw_themes: str) -> Optional[List[str]]:
    """Safely parse and extract theme uuids."""
    # TODO - add escaping
    if raw_themes != constants.ALL_THEMES:
        active_themes = [
            x.strip() for x in raw_themes.split(',')
        ]
    else:
        active_themes = None

    if active_themes == ['']:
        active_themes = None

    return active_themes
