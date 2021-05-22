# -*- coding: utf-8 -*-

"""Main control tool.

Possible call variants:

    To create migrations:
        python manage.py makemigrations
        python manage.py makemigrations all
        python manage.py makemigrations all all
        python manage.py makemigrations source_folder_1
        python manage.py makemigrations source_folder_1 all
        python manage.py makemigrations source_folder_1 leaf_folder_1

        Can add --sources to specify sources dir.
        Can add --content to specify content dir.

    To perform migrations:
        python manage.py migrate
        python manage.py migrate all
        python manage.py migrate all all
        python manage.py migrate source_folder_1
        python manage.py migrate source_folder_1 all
        python manage.py migrate source_folder_1 leaf_folder_1

        Can add --sources to specify sources dir.
        Can add --content to specify content dir.

    To synchronize databases:
        python manage.py sync - from all leaves to all trunks
                                and then everything to root
        python manage.py sync trunk source_folder_1 - from all leaves
                                                      into trunk database
                                                      and then trunk to root
        python manage.py sync leaf leaf_folder_1 - from specified leaf into
                                                   trunk and then to root

        Can add --nocopy to avoid copying new root database to the content dir.

    To launch development server:
        python manage.py runserver
        python manage.py runserver 9000
        python manage.py runserver 127.0.0.1:9000
"""
import os
import sys
from typing import List

from omoide import core
from omoide.use_cases import cli
from omoide.use_cases.makemigrations import makemigrations


def main(args: List[str], *,
         filesystem: core.Filesystem = core.Filesystem(),
         stdout: core.STDOut = core.STDOut()) -> None:
    """Entry point."""
    if not args:
        return

    source_path = os.environ.get('OMOIDE_SOURCE')
    content_path = os.environ.get('OMOIDE_CONTENT')

    operation = cli.parse_arguments(args, source_path, content_path)

    if isinstance(operation, cli.MakeMigrationCommand):
        perform_makemigrations(operation, filesystem, stdout)

    elif isinstance(operation, cli.MigrateCommand):
        perform_migrate(operation, filesystem, stdout)

    elif isinstance(operation, cli.SyncCommand):
        perform_sync(operation, filesystem, stdout)

    else:
        assert isinstance(operation, cli.RunserverCommand)
        perform_runserver(operation, filesystem, stdout)


def perform_makemigrations(command: cli.MakeMigrationCommand,
                           filesystem: core.Filesystem,
                           stdout: core.STDOut) -> None:
    """Perform command."""
    if not filesystem.exists(command.sources_path):
        raise FileNotFoundError(
            f'Sources folder {command.sources_path} does not exist'
        )

    if command.trunk == 'all':
        if command.leaf == 'all':
            makemigrations.all_sources(command, filesystem, stdout)
        else:
            makemigrations.one_leaf(command, filesystem, stdout)
    else:
        makemigrations.one_one_trunk(command, filesystem, stdout)


def perform_migrate(command: cli.MigrateCommand, filesystem: core.Filesystem,
                    stdout: core.STDOut) -> None:
    """Perform command."""
    stdout.print('Applying migrations')
    # TODO


def perform_sync(command: cli.SyncCommand, filesystem: core.Filesystem,
                 stdout: core.STDOut) -> None:
    """Perform command."""
    stdout.print('Synchronizing databases')
    # TODO


def perform_runserver(command: cli.RunserverCommand,
                      filesystem: core.Filesystem,
                      stdout: core.STDOut) -> None:
    """Perform command."""
    stdout.print('Starting server')
    # TODO


if __name__ == '__main__':
    main(sys.argv[1:])
