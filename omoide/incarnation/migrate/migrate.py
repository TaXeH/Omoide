# -*- coding: utf-8 -*-

"""Migrate.
"""
import sqlalchemy as sa

from omoide import commands
from omoide import constants
from omoide import rite
from omoide.database import operations


def act(command: commands.MigrateCommand,
        filesystem: rite.Filesystem,
        stdout: rite.STDOut) -> int:
    """Migrate."""
    total_new_migrations = 0
    walk = commands.walk_storage_from_command(command, filesystem)

    for branch, leaf, leaf_folder in walk:
        migration_file = filesystem.join(leaf_folder,
                                         constants.MIGRATION_FILE_NAME)

        if not filesystem.exists(migration_file):
            stdout.print(f'\t[{branch}][{leaf}] Nothing to migrate')
            continue

        local_db_file = filesystem.join(leaf_folder,
                                        constants.LEAF_DB_FILE_NAME)

        if filesystem.exists(local_db_file):
            filesystem.delete_file(local_db_file)
            stdout.yellow(
                f'\t[{branch}][{leaf}] Deleted {constants.LEAF_DB_FILE_NAME}'
            )

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
        stdout.yellow(f'\t[{branch}][{leaf}] Saved migrations')

    return total_new_migrations
