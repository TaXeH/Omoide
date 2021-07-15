# -*- coding: utf-8 -*-

"""Make migrations.
"""
from typing import List

import omoide.use_cases.make_migrations.saving
from omoide import core, constants, use_cases
from omoide.use_cases import commands, identity
from omoide.use_cases.make_migrations import schema


def act(command: use_cases.MakeMigrationsCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Make migrations."""
    walk = use_cases.utils.walk_storage_from_command(command, filesystem)

    router = use_cases.Router()
    identity_master = use_cases.IdentityMaster()
    uuid_master = use_cases.UUIDMaster()

    identity.gather_existing_identities(command.sources_folder,
                                        router,
                                        identity_master,
                                        uuid_master,
                                        filesystem)

    total_migrations = 0
    for branch, leaf, leaf_folder in walk:
        unit_file_path = filesystem.join(leaf_folder, constants.UNIT_FILE_NAME)

        if filesystem.not_exists(unit_file_path):
            stdout.gray(f'Unit file does not exist: {unit_file_path}')
            continue

        content = filesystem.read_json(unit_file_path)
        new_migrations = schema.instantiate_commands(content=content)
        migration_path = use_cases.make_migrations.saving.save_migrations(
            leaf_folder=leaf_folder,
            migrations=new_migrations,
            filesystem=filesystem,
        )
        stdout.green(f'Created migration file: {migration_path}')
        total_migrations += len(new_migrations)

    return total_migrations


if __name__ == '__main__':
    _command = commands.MakeMigrationsCommand(
        branch='all',
        leaf='all',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        storage_folder='D:\\PycharmProjects\\Omoide\\example\\storage',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
