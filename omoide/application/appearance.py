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


def get_placeholder(current_realm_name: str, current_theme_name: str) -> str:
    """Return specific placeholder if we're not in default theme."""
    if current_theme_name:
        return f'Search on theme "{current_theme_name}"'

    if current_realm_name:
        return f'Search on realm "{current_realm_name}"'

    return ''
