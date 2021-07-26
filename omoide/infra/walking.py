# -*- coding: utf-8 -*-

"""Files/folders iteration tools.
"""
from typing import Iterator, Tuple

from omoide import infra
from omoide.commands import instances

__all__ = [
    'walk_sources_from_command',
    'walk_storage_from_command',
    'walk',
]


def walk_sources_from_command(command: instances.FilesRelatedCommand,
                              filesystem: infra.Filesystem
                              ) -> Iterator[Tuple[str, str, str]]:
    """Typical iteration by command settings."""
    return walk(command.sources_folder, filesystem,
                command.branch, command.leaf)


def walk_storage_from_command(command: instances.FilesRelatedCommand,
                              filesystem: infra.Filesystem
                              ) -> Iterator[Tuple[str, str, str]]:
    """Typical iteration by command settings."""
    return walk(command.storage_folder, filesystem,
                command.branch, command.leaf)


def walk(folder: str, filesystem: infra.Filesystem, branch: str = 'all',
         leaf: str = 'all') -> Iterator[Tuple[str, str, str]]:
    """Iterate on nested folders."""
    for current_branch in filesystem.list_folders(folder):
        if branch != 'all' and branch != current_branch:
            continue

        branch_folder = filesystem.join(folder, current_branch)
        for current_leaf in filesystem.list_folders(branch_folder):

            if leaf != 'all' and leaf != current_leaf:
                continue

            leaf_folder = filesystem.join(branch_folder, current_leaf)

            yield current_branch, current_leaf, leaf_folder