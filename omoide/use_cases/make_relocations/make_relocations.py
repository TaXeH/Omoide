# -*- coding: utf-8 -*-

"""Make relocations.
"""
from typing import List

from omoide import core, constants
from omoide.files.operations import drop_files
from omoide.use_cases import commands, identity
from omoide.use_cases.unite import saving


def act(command: commands.MakeRelocationsCommand, filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Make relocations."""
    filenames_to_delete = {
        constants.RELOCATION_FILENAME,
    }
    drop_files(command, filenames_to_delete, filesystem, stdout)

    router = core.Router()
    identity_master = core.IdentityMaster()
    uuid_master = core.UUIDMaster()

    identity.gather_existing_identities(command.sources_folder,
                                        router,
                                        identity_master,
                                        uuid_master,
                                        filesystem)

    total_relocations = 0
    for branch in filesystem.list_folders(command.sources_folder):

        if command.branch != 'all' and command.branch != branch:
            continue

        branch_folder = filesystem.join(command.sources_folder, branch)
        for leaf in filesystem.list_folders(branch_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(branch_folder, leaf)
            unit_file = filesystem.join(leaf_folder, constants.UNIT_FILENAME)

            if filesystem.not_exists(unit_file):
                continue

            relocations: List[core.Relocation] = []
            content = filesystem.read_json(unit_file)
            for meta in content.get('metas', []):
                new_relocations = make_relocations_for_one_meta(
                    meta=meta,
                    branch=branch,
                    leaf=leaf,
                    sources_folder=command.sources_folder,
                    content_folder=command.content_folder,
                    router=router,
                    filesystem=filesystem,
                )
                relocations.extend(new_relocations)
                total_relocations += len(new_relocations)

            saving.save_relocations(leaf_folder, relocations, filesystem)
            # TODO - get filename here
            stdout.yellow(f'Saved relocations {leaf_folder}')

    return total_relocations


def make_relocations_for_one_meta(meta: dict,
                                  branch: str,
                                  leaf: str,
                                  sources_folder: str,
                                  content_folder: str,
                                  router: core.Router,
                                  filesystem: core.Filesystem):
    relocations: List[core.Relocation] = []
    uuid = meta['uuid']
    realm_uuid = meta['_realm_uuid']
    theme_uuid = meta['_theme_uuid']
    group_uuid = meta['group_uuid']
    filename = meta['original_filename']
    ext = meta['original_extension']

    path_from = filesystem.join(
        sources_folder,
        branch,
        leaf,
        router.get_route(realm_uuid),
        router.get_route(theme_uuid),
        router.get_route(group_uuid),
        f'{filename}.{ext}',
    )

    path_to = filesystem.join(
        content_folder,
        router.get_route(realm_uuid),
        router.get_route(theme_uuid),
        router.get_route(group_uuid),
        f'{uuid}.{ext}'
    )

    new_relocation = core.Relocation(
        uuid=uuid,
        path_from=path_from,
        path_to=path_to,
        width=meta['width'],
        height=meta['height'],
        operation_type='copy',
    )
    relocations.append(new_relocation)

    for (width, height) in constants.COMPRESS_TO:
        new_relocation = core.Relocation(
            uuid=uuid,
            path_from=path_from,
            path_to=path_to,
            width=width,
            height=height,
            operation_type='scale',
        )
        relocations.append(new_relocation)
    return relocations


if __name__ == '__main__':
    _command = commands.MakeRelocationsCommand(
        branch='all',
        leaf='all',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
