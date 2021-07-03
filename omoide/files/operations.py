# -*- coding: utf-8 -*-

"""Basic file operations.
"""
from typing import Collection

from omoide import core


def drop_files(target_folder: str, filenames: Collection[str],
               filesystem: core.Filesystem, stdout: core.STDOut) -> None:
    """Drop all given filenames."""
    filenames = set(filenames)

    for folder, filename, _, _ in filesystem.iter_ext(target_folder):
        if filename in filenames:
            path = filesystem.join(folder, filename)
            # filesystem.delete_file(path)  # FIXME
            stdout.print(f'Dropped file: {path}')