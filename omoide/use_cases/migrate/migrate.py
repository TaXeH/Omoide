# -*- coding: utf-8 -*-

"""Migrate.
"""
import sqlalchemy as sa

from omoide import core, constants, use_cases
from omoide.database import operations
from omoide.use_cases import commands


def act(command: use_cases.MigrateCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Migrate."""
    total_new_migrations = 0
    walk = use_cases.utils.walk_storage_from_command(command, filesystem)

    for branch, leaf, leaf_folder in walk:
        migration_file = filesystem.join(leaf_folder,
                                         constants.MIGRATION_FILE_NAME)

        if not filesystem.exists(migration_file):
            stdout.print(f'Nothing to migrate in {leaf_folder}')
            continue

        local_db_file = filesystem.join(leaf_folder,
                                        constants.LEAF_DB_FILE_NAME)

        if filesystem.exists(local_db_file):
            filesystem.delete_file(local_db_file)
            stdout.yellow(f'Deleted {local_db_file}')

        engine = operations.restore_database_from_scratch(
            folder=leaf_folder,
            filename=constants.LEAF_DB_FILE_NAME,
            filesystem=filesystem,
            stdout=stdout,
            echo=True
        )

        content = filesystem.read_file(migration_file)
        migrations = content.split(';')

        with engine.connect() as conn:
            trans = conn.begin()
            try:
                for migration in migrations:
                    conn.execute(sa.text(migration))
                trans.commit()
            except Exception:
                trans.rollback()
                raise

        total_new_migrations += len(migrations)
        stdout.yellow(f'Saved migrations {local_db_file}')

    return total_new_migrations


if __name__ == '__main__':
    _command = commands.MigrateCommand(
        branch='all',
        leaf='all',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        storage_folder='D:\\PycharmProjects\\Omoide\\example\\storage',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
