# -*- coding: utf-8 -*-

"""Sync.
"""
from sqlalchemy.orm import sessionmaker

from omoide import commands
from omoide import constants
from omoide import rite
from omoide.database import operations
from omoide.database.operations import synchronize


def act(command: commands.SyncCommand,
        filesystem: rite.Filesystem,
        stdout: rite.STDOut) -> int:
    """Sync."""
    root_db_file = filesystem.join(
        command.storage_folder, constants.ROOT_DB_FILE_NAME
    )

    needs_schema = filesystem.not_exists(root_db_file)
    root_db = operations.create_database(
        folder=command.storage_folder,
        filename=constants.ROOT_DB_FILE_NAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )
    if needs_schema:
        operations.create_scheme(root_db, stdout)

    SessionRoot = sessionmaker(bind=root_db)
    session_root = SessionRoot()

    total_migrations = 0
    for branch in filesystem.list_folders(command.storage_folder):

        if command.branch != 'all' and command.branch != branch:
            continue

        branch_folder = filesystem.join(command.storage_folder, branch)
        branch_db_file = filesystem.join(branch_folder,
                                         constants.BRANCH_DB_FILE_NAME)
        needs_schema = filesystem.not_exists(branch_db_file)
        branch_db = operations.create_database(
            folder=branch_folder,
            filename=constants.BRANCH_DB_FILE_NAME,
            filesystem=filesystem,
            stdout=stdout,
            echo=True,
        )
        if needs_schema:
            operations.create_scheme(branch_db, stdout)

        SessionBranch = sessionmaker(bind=branch_db)
        session_branch = SessionBranch()

        for leaf in filesystem.list_folders(branch_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(branch_folder, leaf)
            leaf_db_file = filesystem.join(leaf_folder,
                                           constants.LEAF_DB_FILE_NAME)

            if not filesystem.exists(leaf_db_file):
                stdout.print(f'\t[{branch}][{leaf}] Nothing to migrate')
                continue

            spacer = '  ' + len(branch) * ' '

            leaf_db = operations.create_database(
                folder=leaf_folder,
                filename=constants.LEAF_DB_FILE_NAME,
                filesystem=filesystem,
                stdout=stdout,
                echo=True,
            )
            SessionLeaf = sessionmaker(bind=leaf_db)
            session_leaf = SessionLeaf()

            synchronize(session_from=session_leaf, session_to=session_branch)
            total_migrations += 1
            stdout.yellow(f'\t{spacer}[{leaf}] Synchronized')

        synchronize(session_from=session_branch, session_to=session_root)
        total_migrations += 1
        stdout.yellow(f'\t[{branch}] Synchronized')

    return total_migrations
