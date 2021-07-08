# -*- coding: utf-8 -*-

"""Make migrations.
"""
from typing import List

from omoide import core, constants
from omoide.files.operations import drop_files
from omoide.use_cases import commands, identity
from omoide.use_cases.make_migrations import schema
from omoide.use_cases.unite import saving


def act(command: commands.MakeRelocationsCommand, filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Make migrations."""
    filenames_to_delete = {
        constants.MIGRATION_FILE_NAME,
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

    total_migrations = 0
    for branch in filesystem.list_folders(command.sources_folder):

        if command.branch != 'all' and command.branch != branch:
            continue

        branch_folder = filesystem.join(command.sources_folder, branch)
        for leaf in filesystem.list_folders(branch_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(branch_folder, leaf)
            unit_file = filesystem.join(leaf_folder, constants.UNIT_FILE_NAME)

            if filesystem.not_exists(unit_file):
                continue

            content = filesystem.read_json(unit_file)
            new_migrations = schema.instantiate_commands(content=content)
            saving.save_migrations(leaf_folder, new_migrations, filesystem)
            # TODO - get filename here
            stdout.yellow(f'Saved migrations {leaf_folder}')
            total_migrations += len(new_migrations)

    return total_migrations


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
