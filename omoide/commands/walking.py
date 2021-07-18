# -*- coding: utf-8 -*-

"""Files/folders iteration tools.
"""
from typing import Iterator, Tuple

from omoide import rite
from omoide.commands import instances

__all__ = [
    'walk_sources_from_command',
    'walk_storage_from_command',
]


def walk_sources_from_command(command: instances.FilesRelatedCommand,
                              filesystem: rite.Filesystem
                              ) -> Iterator[Tuple[str, str, str]]:
    """Typical iteration by command settings."""
    return rite.walk(command.sources_folder, filesystem,
                     command.branch, command.leaf)


def walk_storage_from_command(command: instances.FilesRelatedCommand,
                              filesystem: rite.Filesystem
                              ) -> Iterator[Tuple[str, str, str]]:
    """Typical iteration by command settings."""
    return rite.walk(command.storage_folder, filesystem,
                     command.branch, command.leaf)
