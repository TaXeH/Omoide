# -*- coding: utf-8 -*-

"""Relocate.
"""
from omoide import use_cases, core, constants


def act(command: use_cases.RelocateCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Make relocations."""
    renderer = use_cases.Renderer()
    walk = use_cases.utils.walk_sources_from_command(command, filesystem)

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
        relocations = [core.Relocation(**x) for x in raw_relocations]
        total_new_relocations += len(relocations)

        for relocation in relocations:
            relocate_single_file(relocation, renderer, filesystem, stdout)

    return total_new_relocations


def relocate_single_file(relocation: core.Relocation,
                         renderer: use_cases.Renderer,
                         filesystem: core.Filesystem,
                         stdout: core.STDOut) -> None:
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
