# -*- coding: utf-8 -*-
"""Display folder tree.
"""
from collections import defaultdict

from omoide import commands
from omoide import rite


def act(command: commands.ShowTreeCommand,
        filesystem: rite.Filesystem,
        stdout: rite.STDOut) -> int:
    """Display folder tree."""
    walk = commands.walk_sources_from_command(command, filesystem)
    tree = defaultdict(list)

    total = 0
    for branch, leaf, _ in walk:
        tree[branch].append(leaf)
        total += 1

    print(tree)
    return total
