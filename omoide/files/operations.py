# -*- coding: utf-8 -*-

"""Basic file operations.
"""
from typing import Collection

from omoide import core
from omoide.use_cases import commands


def drop_files(command: commands.BaseCommand,
               filenames_to_delete: Collection[str],
               filesystem: core.Filesystem, stdout: core.STDOut) -> None:
    """Drop all given filenames."""
    filenames_to_delete = set(filenames_to_delete)
    files_to_delete = []

    for branch in filesystem.list_folders(command.sources_folder):

        if command.branch != 'all' and command.branch != branch:
            continue

        branch_folder = filesystem.join(command.sources_folder, branch)
        files_to_delete.extend(
            filesystem.join(branch_folder, filename)
            for filename in filesystem.list_files(branch_folder)
            if filename in filenames_to_delete
        )

        for leaf in filesystem.list_folders(branch_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(branch_folder, leaf)
            files_to_delete.extend(
                filesystem.join(leaf_folder, filename)
                for filename in filesystem.list_files(leaf_folder)
                if filename in filenames_to_delete
            )

    for file in files_to_delete:
        # filesystem.delete_file(path)  # FIXME
        stdout.print(f'Dropped file: {file}')
