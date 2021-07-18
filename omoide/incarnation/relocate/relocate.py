# -*- coding: utf-8 -*-

"""Relocate.
"""
from omoide import commands
from omoide import constants
from omoide import essence
from omoide import rite


def act(command: commands.RelocateCommand,
        filesystem: rite.Filesystem,
        stdout: rite.STDOut) -> int:
    """Make relocations."""
    renderer = essence.Renderer()
    walk = commands.walk_sources_from_command(command, filesystem)

    total_new_relocations = 0
    for branch, leaf, _ in walk:
        storage_folder = filesystem.join(command.storage_folder, branch, leaf)
        relocation_file_path = filesystem.join(storage_folder,
                                               constants.RELOCATION_FILE_NAME)

        if filesystem.not_exists(relocation_file_path):
            stdout.gray(
                f'\t[{branch}][{leaf}] Relocation file does not exist'
            )
            continue

        raw_relocations = filesystem.read_json(relocation_file_path)
        relocations = [essence.Relocation(**x) for x in raw_relocations]
        total_new_relocations += len(relocations)

        for relocation in relocations:
            relocate_single_file(relocation, renderer, filesystem, stdout)

    return total_new_relocations


def relocate_single_file(relocation: essence.Relocation,
                         renderer: essence.Renderer,
                         filesystem: rite.Filesystem,
                         stdout: rite.STDOut) -> None:
    """Save one file."""
    if filesystem.not_exists(relocation.path_from):
        raise FileNotFoundError(
            f'Original media file does not exist: {relocation.path_from}'
        )

    folder = filesystem.cut_tail(relocation.path_to)
    filesystem.ensure_folder_exists(folder, stdout)

    if relocation.operation_type == 'copy':
        filesystem.copy_file(relocation.path_from, relocation.path_to)
        stdout.yellow(
            f'\t\t{relocation.operation_type.title()}: {relocation.filename}'
        )
    else:
        renderer.resize(relocation.path_from, relocation.path_to,
                        relocation.width, relocation.height)
        stdout.green(
            f'\t\t{relocation.operation_type.title()}: {relocation.filename}'
        )
