# -*- coding: utf-8 -*-

"""Sync.
"""
from sqlalchemy.orm import sessionmaker

from omoide import core, constants, use_cases
from omoide.database import models
from omoide.database import operations
from omoide.database.operations import synchronize
from omoide.use_cases import commands

assert models


def act(command: use_cases.SyncCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Sync."""
    root_db_file = filesystem.join(
        command.storage_folder, constants.ROOT_DB_FILE_NAME
    )
    needs_schema = filesystem.not_exists(root_db_file)
    root = operations.create_database(
        folder=command.storage_folder,
        filename=constants.ROOT_DB_FILE_NAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )
    if needs_schema:
        operations.create_scheme(root, stdout)

    SessionRoot = sessionmaker(bind=root)
    session_root = SessionRoot()

    total_migrations = 0
    for branch in filesystem.list_folders(command.storage_folder):

        if command.branch != 'all' and command.branch != branch:
            continue

        branch_folder = filesystem.join(command.storage_folder, branch)
        branch_db_file = filesystem.join(branch_folder,
                                         constants.BRANCH_DB_FILE_NAME)
        needs_schema = filesystem.not_exists(branch_db_file)
        branch = operations.create_database(
            folder=branch_folder,
            filename=constants.BRANCH_DB_FILE_NAME,
            filesystem=filesystem,
            stdout=stdout,
            echo=True,
        )
        if needs_schema:
            operations.create_scheme(branch, stdout)

        SessionBranch = sessionmaker(bind=branch)
        session_branch = SessionBranch()

        for leaf in filesystem.list_folders(branch_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(branch_folder, leaf)
            leaf_db_file = filesystem.join(leaf_folder,
                                           constants.LEAF_DB_FILE_NAME)

            if not filesystem.exists(leaf_db_file):
                stdout.print(f'Nothing to migrate in {leaf_folder}')
                continue

            leaf = operations.create_database(
                folder=leaf_folder,
                filename=constants.LEAF_DB_FILE_NAME,
                filesystem=filesystem,
                stdout=stdout,
                echo=True,
            )
            SessionLeaf = sessionmaker(bind=leaf)
            session_leaf = SessionLeaf()

            synchronize(session_from=session_leaf, session_to=session_branch)
            total_migrations += 1
            stdout.yellow(f'Synchronized {leaf_folder}')

        synchronize(session_from=session_branch, session_to=session_root)
        total_migrations += 1
        stdout.yellow(f'Synchronized {branch_folder}')

    return total_migrations


if __name__ == '__main__':
    _command = commands.SyncCommand(
        branch='all',
        leaf='all',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        storage_folder='D:\\PycharmProjects\\Omoide\\example\\storage',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
