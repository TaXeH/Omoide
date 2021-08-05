# -*- coding: utf-8 -*-
"""Styling things.
"""
from typing import Tuple, List

from omoide import utils, constants


def get_note_on_search(total: int, duration: float) -> str:
    """Return description of search duration."""
    _total = utils.sep_digits(total)
    _duration = '{:0.4f}'.format(duration)

    note = f'Found {_total} records in {_duration} seconds'

    return note


# def format_graph(graph: dict, current_realm: str,
#                  current_theme: str) -> List[Tuple[str, str, str]]:
#     """Prepare graph for rendering."""
#     rows = []
#
#     for realm_uuid, realm_contents in graph.items():
#         if current_realm == realm_uuid \
#                 or current_realm == constants.ALL_REALMS:
#             rows.append(
#                 ('realm_green', realm_uuid, realm_contents['label']),
#             )
#         else:
#             rows.append(
#                 ('realm_red', realm_uuid, realm_contents['label']),
#             )
#
#         for theme_uuid, theme_contents in realm_contents['themes'].items():
#             if current_theme == theme_uuid \
#                     or current_theme == constants.ALL_THEMES:
#                 rows.append(
#                     ('theme_green', theme_uuid, theme_contents['label']),
#                 )
#                 for group in theme_contents['groups']:
#                     rows.append(
#                         ('group_green', '', group),
#                     )
#             else:
#                 rows.append(
#                     ('theme_red', theme_uuid, theme_contents['label']),
#                 )
#                 for group in theme_contents['groups']:
#                     rows.append(
#                         ('group_red', '', group),
#                     )
#
#     return rows
