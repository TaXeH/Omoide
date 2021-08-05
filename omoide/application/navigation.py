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

Resulting terminal output looks like:
    Basic        ──────┬──────Mice and huma──────┬──────History
                       │                         │
                       │                         ├──────As pets
                       │                         │
                       │                         ├──────As model orga
                       │                         │
                       │                         └──────Folk culture
                       │
                       ├──────Life expectan
                       │
                       └──────Life cycle an──────┬──────Polygamy
                                                 │
                                                 └──────Polyandry
"""
from typing import Tuple, List, Dict


class Cell:
    """Regular element of a table."""

    def __init__(self, kind: str,
                 identifier: str = '', label: str = '') -> None:
        """Initialize instance."""
        self.kind = kind
        self.identifier = identifier
        self.label = label

    def __repr__(self) -> str:
        """Return textual representation."""
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

        elif self.kind == 'vertical_line':
            output = '│'.center(width, spacer)

        elif self.kind == 'triplet_bottom':
            output = '┬'.center(width, '─')

        elif self.kind == 'triplet_right':
            output = spacer * (width // 2) + '├' + '─' * (width // 2)

        elif self.kind == 'corner':
            output = spacer * (width // 2) + '└' + '─' * (width // 2)

        else:
            output = '?' * width

        return f'{left}{output}{right}'

    @classmethod
    def empty(cls) -> 'Cell':
        """Create empty instance."""
        return cls(kind='empty')


Table = List[List[Cell]]


def generate_table_header(width: int) -> Table:
    """Create first row of the table."""
    top_row = [
        Cell(kind='text', identifier='all_realms', label='All realms'),
        Cell.empty(),
        Cell(kind='text', identifier='all_themes', label='All themes'),
    ]
    top_tail = [Cell.empty() for _ in range(width - 3)]
    spacer_row = [Cell.empty() for _ in range(width)]
    return [top_row + top_tail, spacer_row]


def calculate_graph_dimensions(graph: dict, *,
                               depth: int = 1) -> Tuple[int, int]:
    """Return width and height of the graph.

    Width corresponds to maximum nesting level and
    defines horizontal size of image, required to draw the graph.

    Height corresponds to amount of terminal (non nested) elements and
    defines how many lines will be used to draw the graph.

    >>> demo = {'x': {'elements': {'y': {}}, 'z': {}}}
    >>> calculate_graph_dimensions(demo)
    (1, 2)
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
    return height + height - 1, width + width - 1


def generate_empty_table(rows: int, cols: int) -> List[List[Cell]]:
    """Generate empty table of given size."""
    return [
        [Cell.empty() for _ in range(cols)] for _ in range(rows)
    ]


def populate_table(table: List[List[Cell]], graph: dict,
                   initials: List[Tuple[int, int]],
                   coordinates: Dict[str, Tuple[int, int]],
                   row: int = 0, col: int = 0) -> int:
    """Transform graph into table contents."""
    row_shift = 0
    total = len(graph)

    for i, (identifier, contents) in enumerate(graph.items(), start=1):
        elements = contents.get('elements', {})
        label = contents.get('label', '???')

        coordinates[identifier] = (row + row_shift, col)
        table[row + row_shift][col] = Cell(kind='text',
                                           identifier=identifier,
                                           label=label)
        if col > 0:
            if i == 1 and total > 1:
                table[row + row_shift][col - 1] = Cell('triplet_bottom')
                initials.append((row, col - 1))
            elif 1 < i < total:
                table[row + row_shift][col - 1] = Cell('triplet_right')
            elif i == total and total > 1:
                table[row + row_shift][col - 1] = Cell('corner')
            else:
                table[row + row_shift][col - 1] = Cell('horizontal_line')

        if elements:
            new_lines = populate_table(table, elements, initials,
                                       coordinates, row + row_shift, col + 2)

            row_shift += max(2, new_lines)
        else:
            row_shift += 2

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

            elif cell.kind == 'corner':
                break


def stringify_table(table: List[List[Cell]],
                    width: int, verbose: bool = False) -> str:
    """Convert table into string."""
    lines = []
    for row in table:
        lines.append(''.join(x.as_str(width, verbose) for x in row))
    return '\n'.join(lines)
