# -*- coding: utf-8 -*-

"""Make relocations.
"""
from dataclasses import asdict
from typing import List

from omoide import constants
from omoide import core
from omoide import use_cases
from omoide.use_cases.common import transient


def act(command: use_cases.MakeRelocationsCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Make relocations."""
    walk = use_cases.utils.walk_sources_from_command(command, filesystem)

    total_new_relocations = 0
    for branch, leaf, _ in walk:
        storage_folder = filesystem.join(command.storage_folder, branch, leaf)
        unit_file_path = filesystem.join(storage_folder,
                                         constants.UNIT_FILE_NAME)

        if filesystem.not_exists(unit_file_path):
            stdout.gray(f'\t[{branch}][{leaf}] Unit file does not exist')
            continue

        relocations: List[core.Relocation] = []
        unit_dict = filesystem.read_json(unit_file_path)
        unit = transient.Unit(**unit_dict)

        for meta in unit.metas:
            new_relocations = make_relocations_for_one_meta(
                command=command,
                meta=meta,
                branch=branch,
                leaf=leaf,
                filesystem=filesystem,
            )
            relocations.extend(new_relocations)
            total_new_relocations += len(new_relocations)

        save_relocations(
            folder=storage_folder,
            relocations=relocations,
            filesystem=filesystem,
        )
        stdout.green(f'\t[{branch}][{leaf}] Created relocation file')

    return total_new_relocations


def make_relocations_for_one_meta(command: use_cases.MakeRelocationsCommand,
                                  meta: transient.Meta,
                                  branch: str,
                                  leaf: str,
                                  filesystem: core.Filesystem):
    """Gather all required for relocation information."""
    relocations: List[core.Relocation] = []

    _, category, realm, theme, group, _ = meta.path_to_content.split('/')

    path_from = filesystem.join(
        command.sources_folder,
        branch,
        leaf,
        realm,
        theme,
        group,
        f'{meta.original_filename}.{meta.original_extension}',
    )

    path_to = filesystem.join(
        command.content_folder,
        category,
        realm,
        theme,
        group,
        f'{meta.uuid}.{meta.original_extension}'
    )

    new_relocation = core.Relocation(
        uuid=meta.uuid,
        filename=f'{meta.original_filename}.{meta.original_extension}',
        path_from=path_from,
        path_to=path_to,
        width=meta.width,
        height=meta.height,
        operation_type='copy',
    )
    relocations.append(new_relocation)

    path_to = filesystem.join(
        command.content_folder,
        'preview',
        realm,
        theme,
        group,
        f'{meta.uuid}.{meta.original_extension}'
    )

    new_relocation = core.Relocation(
        uuid=meta.uuid,
        filename=f'{meta.original_filename}.{meta.original_extension}',
        path_from=path_from,
        path_to=path_to,
        width=constants.PREVIEW_SIZE[0],
        height=constants.PREVIEW_SIZE[1],
        operation_type='scale',
    )
    relocations.append(new_relocation)

    path_to = filesystem.join(
        command.content_folder,
        'thumbnails',
        realm,
        theme,
        group,
        f'{meta.uuid}.{meta.original_extension}'
    )

    new_relocation = core.Relocation(
        uuid=meta.uuid,
        filename=f'{meta.original_filename}.{meta.original_extension}',
        path_from=path_from,
        path_to=path_to,
        width=constants.THUMBNAIL_SIZE[0],
        height=constants.THUMBNAIL_SIZE[1],
        operation_type='scale',
    )
    relocations.append(new_relocation)

    return relocations


def save_relocations(folder: str,
                     relocations: List[core.Relocation],
                     filesystem: core.Filesystem) -> str:
    """Save relocations as JSON file."""
    file_path = filesystem.join(folder, constants.RELOCATION_FILE_NAME)
    filesystem.write_json(file_path, [asdict(x) for x in relocations])
    return file_path
