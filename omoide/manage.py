# -*- coding: utf-8 -*-

"""Main control tool.

Possible call variants:

    To make migrations:
        python manage.py make_migrations
        python manage.py make_migrations all
        python manage.py make_migrations all all
        python manage.py make_migrations source_folder_1
        python manage.py make_migrations source_folder_1 all
        python manage.py make_migrations source_folder_1 leaf_folder_1

    To perform migrations:
        python manage.py migrate
        python manage.py migrate all
        python manage.py migrate all all
        python manage.py migrate source_folder_1
        python manage.py migrate source_folder_1 all
        python manage.py migrate source_folder_1 leaf_folder_1

    To relocate and resize media files:
        python manage.py relocate
        python manage.py relocate all
        python manage.py relocate all all
        python manage.py relocate source_folder_1
        python manage.py relocate source_folder_1 all
        python manage.py relocate source_folder_1 leaf_folder_1

    To synchronize databases:
        python manage.py sync - from all leaves to all trunks
                                and then everything to root
        python manage.py sync trunk source_folder_1 - from all leaves
                                                      into trunk database
                                                      and then trunk to root
        python manage.py sync leaf leaf_folder_1 - from specified leaf into
                                                   trunk and then to root

    To create final static database:
        python manage.py freeze

    To launch development server:
        python manage.py runserver
        python manage.py runserver 9000
        python manage.py runserver 127.0.0.1:9000

    Use --sources to specify sources folder.
    Use --content to specify content folder.
"""
import os
import sys
from typing import List

from omoide import core
from omoide.use_cases import cli
from omoide.use_cases import commands
from omoide.use_cases.make_migrations import make_migrations


def main(args: List[str], *,
         filesystem: core.Filesystem = core.Filesystem(),
         stdout: core.STDOut = core.STDOut()) -> None:
    """Entry point."""
    if not args:
        stdout.yellow('No arguments to parse')
        return

    source_path = os.environ.get('OMOIDE_SOURCE')
    content_path = os.environ.get('OMOIDE_CONTENT')

    operation = cli.parse_arguments(args, source_path, content_path)

    if isinstance(operation, commands.MakeMigrationsCommand):
        perform_make_migrations(operation, filesystem, stdout)

    elif isinstance(operation, commands.MigrateCommand):
        perform_migrate(operation, filesystem, stdout)

    elif isinstance(operation, commands.RelocateCommand):
        perform_relocate(operation, filesystem, stdout)

    elif isinstance(operation, commands.SyncCommand):
        perform_sync(operation, filesystem, stdout)

    elif isinstance(operation, commands.FreezeCommand):
        perform_freeze(operation, filesystem, stdout)

    else:
        assert isinstance(operation, commands.RunserverCommand)
        perform_runserver(operation, filesystem, stdout)


def perform_make_migrations(
        command: commands.MakeMigrationsCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> None:
    """Perform make_migrations command."""
    stdout.print('Creating migrations')

    if not filesystem.exists(command.sources_folder):
        raise FileNotFoundError(
            f'Sources folder {command.sources_folder} does not exist'
        )

    if not filesystem.exists(command.content_folder):
        filesystem.ensure_folder_exists(command.content_folder, stdout)

    total = make_migrations.act(command, filesystem, stdout)
    stdout.print(f'Total {total} migrations created')


def perform_migrate(command: commands.MigrateCommand,
                    filesystem: core.Filesystem,
                    stdout: core.STDOut) -> None:
    """Perform migration command."""
    stdout.print('Applying migrations')
    # TODO


def perform_relocate(command: commands.RelocateCommand,
                     filesystem: core.Filesystem,
                     stdout: core.STDOut) -> None:
    """Perform relocation command."""
    stdout.print('Applying relocations')
    # TODO


def perform_sync(command: commands.SyncCommand,
                 filesystem: core.Filesystem,
                 stdout: core.STDOut) -> None:
    """Perform sync command."""
    stdout.print('Synchronizing databases')
    # TODO


def perform_freeze(command: commands.FreezeCommand,
                   filesystem: core.Filesystem,
                   stdout: core.STDOut) -> None:
    """Perform freeze command."""
    stdout.print('Making static database')
    # TODO


def perform_runserver(command: commands.RunserverCommand,
                      filesystem: core.Filesystem,
                      stdout: core.STDOut) -> None:
    """Perform command."""
    stdout.print('Starting server')
    # TODO


if __name__ == '__main__':
    main(sys.argv[1:])
