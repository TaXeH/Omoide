# -*- coding: utf-8 -*-
"""Site map building tools.

Mostly this module is created to handle printing/drawing of the navigation tab.

This is typical graph printing problem.
Usual approach to this is to print it line by line:

    root  <-- top level entity
    ├── file
    ├── folder  <-- middle level entity
    │   ├── folder  <-- lower level entity
    │   │   └── ...
    │   └── file
    └── folder
        ├── folder
        │   └── ...
        └── file

In this case one unit of information takes single line.
It is handy, but takes a lot of place. Instead I wanted to print it more
compact, but I had to mix different entities in single line.

Resulting algorithm is less efficient than it could be, but I prefer
using simple code instead of fighting for CPU usage.
"""
from itertools import chain, repeat
from typing import Tuple, List

reference_graph = {
    'A': {
        'label': 'Basic',
        'elements': {
            'A-1': {
                'label': 'Mice and humans',
                'elements': {
                    'A-1-1': {
                        'label': 'History',
                    },
                    'A-1-2': {
                        'label': 'As pets',
                    },
                    'A-1-3': {
                        'label': 'As model organism',
                    },
                    'A-1-4': {
                        'label': 'Folk culture',
                    },
                }
            },
            'A-2': {
                'label': 'Life expectancy',
            },
            'A-3': {
                'label': 'Life cycle and reproduction',
                'elements': {
                    'A-3-1': {
                        'label': 'Polygamy',
                    },
                    'A-3-2': {
                        'label': 'Polyandry',
                    },
                }
            }
        },
    },
    'B': {
        'label': 'Animalia',
    },
    'C': {
        'label': 'Senses',
        'elements': {
            'C-1': {
                'label': 'Vision'
            },
            'C-2': {
                'label': 'Olfaction'
            },
            'C-3': {
                'label': 'Tactile'
            },
        },
    },
    'D': {
        'label': 'Behavior',
        'elements': {
            'D-1': {
                'label': 'Social behavior'
            }
        }
    }
}


# @dataclass
# class ContentType:
#     """Possible content of table cell."""
#     kind: str = 'empty'
#
#
# @dataclass
# class ContentTypeGeometry(ContentType):
#     """Possible geometric content of table cell."""
#     is_active: bool = False
#
#
# @dataclass
# class ContentEmpty(ContentType):
#     """Empty cell."""
#     kind = 'empty'
#
#     def __repr__(self):
#         return ' '.center(19, ' ')
#
#
# @dataclass
# class ContentHorLine(ContentTypeGeometry):
#     """Horizontal line."""
#     kind = 'horizontal_line'
#
#     def __repr__(self):
#         if self.is_active:
#             return '═' * 19
#         return '─' * 19
#
#
# @dataclass
# class ContentVerLine(ContentTypeGeometry):
#     """Horizontal line."""
#     kind = 'vertical_line'
#
#     def __repr__(self):
#         if self.is_active:
#             return '║'.center(19, ' ')
#         return '│'.center(19, ' ')
#
#
# @dataclass
# class ContentCorner(ContentTypeGeometry):
#     """Turning line."""
#     kind = 'corner_line'
#
#     def __repr__(self):
#         if self.is_active:
#             return '         ╚═════════'
#         return '         └─────────'
#
#
# @dataclass
# class ContentBottomTriple(ContentTypeGeometry):
#     """Turning line."""
#     kind = 'bottom_triple'
#
#     def __repr__(self):
#         if self.is_active:
#             return '╦'.center(19, '═')
#         return '┬'.center(19, '─')
#
#
# @dataclass
# class ContentRightTriple(ContentTypeGeometry):
#     """Turning line."""
#     kind = 'right_triple'
#
#     def __repr__(self):
#         if self.is_active:
#             return '         ╠═════════'
#         return '         ├─────────'
#
#
# @dataclass
# class ContentButton(ContentType):
#     """Realm/theme/group."""
#     link: str = ''
#     label: str = '?'
#     kind = 'button'
#
#     def __repr__(self):
#         return '{:19}'.format(self.label[:19])
#
#
# def is_active_realm(current_realm: str) -> str:
#     """Choose style for realm."""
#     if current_realm == constants.ALL_REALMS:
#         return 'active_button'
#     return 'passive_button'
#
#
# def is_active_theme(current_theme: str) -> str:
#     """Choose style for theme."""
#     if current_theme == constants.ALL_THEMES:
#         return 'active_button'
#     return 'passive_button'


# def create_first_table_row(current_realm: str,
#                            current_theme: str) -> List[ContentType]:
#     """Create first row of the table."""
#     return [
#         ContentButton(style=is_active_realm(current_realm),
#                       link=constants.ALL_REALMS,
#                       label='All realms'),
#         ContentGeometry(style='empty_geometry'),
#         ContentButton(style=is_active_theme(current_theme),
#                       link=constants.ALL_THEMES,
#                       label='All themes'),
#         ContentGeometry(style='empty_geometry'),
#         ContentGeometry(style='empty_geometry'),
#     ]


# def _empty_table_row() -> TableRow:
#     """Create empty row of the table."""
#     row = TableRow(
#         cells=[ContentGeometry(style='empty_geometry')] * 5
#     )
#     return row


# def generate_navigation_table(graph: dict, current_realm: str,
#                               current_theme: str) -> List[TableRow]:
#     """Create model for navigation table."""
#     table = [
#         _first_table_row(current_realm, current_theme),
#         _empty_table_row(),
#     ]
#
#     sequence: List[ContentType] = []
#     for realm_uuid, realm_contents in graph.items():
#         sequence.append(ContentButton(style=is_active_realm(current_realm),
#                                       link=realm_uuid,
#                                       label=realm_contents['label']))
#
#         elements = realm_contents.get('elements', {})
#         if elements:
#             sequence.append(ContentGeometry(style='horizontal_line'))
#             generate_sub_unit(sequence, realm_contents['elements'],
#                               current_theme)
#         else:
#             sequence.append(ContentGeometry(style='empty_geometry'))
#             sequence.append(ContentGeometry(style='empty_geometry'))
#             sequence.append(ContentGeometry(style='empty_geometry'))
#             sequence.append(ContentGeometry(style='empty_geometry'))
#
#     for line in utils.group_to_size(sequence, 5):
#         table.append(TableRow(cells=list(line)))
#     return table


class Cell:
    """Regular element of a table."""

    def __init__(self, kind: str, identifier: str = '',
                 label: str = '') -> None:
        """Initialize instance."""
        self.kind = kind
        self.identifier = identifier
        self.label = label

    def __repr__(self):
        return self.kind

    def as_str(self, width: int, verbose: bool) -> str:
        """Convert into printable string."""
        assert width % 2 != 0
        spacer = ' ' if not verbose else '_'
        left = '' if not verbose else '['
        right = '' if not verbose else ']'

        if self.kind == 'empty':
            output = spacer * width
        elif self.kind == 'text':
            output = self.label[:width].ljust(width, spacer)

        elif self.kind == 'horizontal_line':
            output = '─' * width
        elif self.kind == 'horizontal_line_active':
            output = '═' * width

        elif self.kind == 'vertical_line':
            output = '│'.center(width, spacer)
        elif self.kind == 'vertical_line_active':
            output = '║'.center(width, spacer)

        elif self.kind == 'triplet_bottom':
            output = '┬'.center(width, '─')
        elif self.kind == 'triplet_bottom_active':
            output = '┬'.center(width, '─')
        elif self.kind == 'triplet_bottom_semi_active':
            output = '╤'.center(width, '═')
        elif self.kind == 'triplet_right':
            output = spacer * (width // 2) + '├' + '─' * (width // 2)
        elif self.kind == 'triplet_right_active':
            output = spacer * (width // 2) + '╠' + '═' * (width // 2)
        elif self.kind == 'triplet_right_semi_active':
            output = spacer * (width // 2) + '╞' + '═' * (width // 2)

        elif self.kind == 'corner':
            output = spacer * (width // 2) + '└' + '─' * (width // 2)
        elif self.kind == 'corner_active':
            output = spacer * (width // 2) + '╚' + '═' * (width // 2)
        else:
            output = '?' * width

        return f'{left}{output}{right}'

    @classmethod
    def empty(cls) -> 'Cell':
        """Create empty instance."""
        return cls(kind='empty')


def calculate_graph_dimensions(graph: dict, *,
                               depth: int = 1) -> Tuple[int, int]:
    """Return width and height of the graph.

    Width corresponds to maximum nesting level and
    defines horizontal size of image, required to draw the graph.

    Height corresponds to amount of terminal (non nested) elements and
    defines how many lines will be used to draw the graph.
    """
    height = 0
    max_depth = depth

    for contents in graph.values():
        elements = contents.get('elements', {})

        if elements:
            new_height, new_depth = calculate_graph_dimensions(
                graph=elements,
                depth=depth + 1,
            )
            height += new_height
            max_depth = max(depth, new_depth, max_depth)
        else:
            height += 1

    return height, max_depth


def calculate_table_dimensions(graph: dict) -> Tuple[int, int]:
    """Return amount of (rows, cols) needed to build a table."""
    height, width = calculate_graph_dimensions(graph)
    return height, width + width - 1  # FIXME


def generate_empty_table(rows: int, cols: int) -> List[List[Cell]]:
    """Generate empty table of given size."""
    return [
        [Cell.empty() for _ in range(cols)] for _ in range(rows)
    ]


def extend_highlight(highlight: List[str], table_width: int) -> List[str]:
    """Extend highlight to a full table size.

    >>> extend_highlight(['a', 'b'], table_width=7)
    ['a', '', 'b', '', 'all', '', 'all']
    """
    graph_width = table_width - (table_width // 2)
    output: List[str] = highlight + ['all'] * (graph_width - len(highlight))
    output = list(chain.from_iterable(zip(output, repeat(''))))

    if output[-1] == '':
        output.pop()

    return output


def populate_table(table: List[List[Cell]], graph: dict,
                   initials: List[Tuple[int, int]],
                   row: int = 0, col: int = 0) -> int:
    """Transform graph into table contents."""
    row_shift = 0
    total = len(graph)

    for i, (identifier, contents) in enumerate(graph.items(), start=1):
        elements = contents.get('elements', {})

        table[row + row_shift][col] = Cell(
            kind='text',
            identifier=identifier,
            label=contents['label'],
        )

        if col > 0:
            if i == 1 and total > 1:
                table[row + row_shift][col - 1] = Cell(
                    f'triplet_bottom'
                )
                initials.append((row, col - 1))
            elif 1 < i < total:
                table[row + row_shift][col - 1] = Cell(
                    f'triplet_right'
                )
            elif i == total and total > 1:
                table[row + row_shift][col - 1] = Cell(
                    f'corner'
                )
            else:
                table[row + row_shift][col - 1] = Cell(
                    f'horizontal_line'
                )

        if elements:
            new_lines = populate_table(table, elements, initials,
                                       row + row_shift, col + 2)

            row_shift += max(1, new_lines)
        else:
            row_shift += 1

    return row_shift


def continue_lines(table: List[List[Cell]],
                   initials: List[Tuple[int, int]]) -> None:
    """Fill missing lines in table."""
    total = len(table)
    for row, col in initials:
        for sub_row in range(row + 1, total):
            cell = table[sub_row][col]

            if cell.kind == 'empty':
                table[sub_row][col] = Cell('vertical_line')
            elif cell.kind in ('corner', 'corner_active'):
                break


def stringify_table(table: List[List[Cell]],
                    width: int, verbose: bool = False) -> str:
    """Convert table into string."""
    lines = []
    for row in table:
        lines.append(''.join(x.as_str(width, verbose) for x in row))
    return '\n'.join(lines)


def main():
    rows, cols = calculate_table_dimensions(reference_graph)
    table = generate_empty_table(rows, cols)
    initials = []
    # highlight = ['A', 'A-3']
    populate_table(table, reference_graph, initials)
    continue_lines(table, initials)
    text = stringify_table(table, width=13, verbose=False)
    print(text)


if __name__ == '__main__':
    main()
