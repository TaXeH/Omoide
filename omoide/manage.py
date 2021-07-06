# -*- coding: utf-8 -*-

"""Main control tool.

Possible call variants:

    To analyze source files and create unit files:
        python manage.py unite
        python manage.py unite all
        python manage.py unite all all
        python manage.py unite source_folder_1
        python manage.py unite source_folder_1 all
        python manage.py unite source_folder_1 leaf_folder_1

    To make migrations:
        python manage.py make_migrations
        python manage.py make_migrations all
        python manage.py make_migrations all all
        python manage.py make_migrations source_folder_1
        python manage.py make_migrations source_folder_1 all
        python manage.py make_migrations source_folder_1 leaf_folder_1

    To make relocations:
        python manage.py make_relocations
        python manage.py make_relocations all
        python manage.py make_relocations all all
        python manage.py make_relocations source_folder_1
        python manage.py make_relocations source_folder_1 all
        python manage.py make_relocations source_folder_1 leaf_folder_1

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

    For all commands:
        Use --sources to specify sources folder.
        Use --content to specify content folder.
"""
import os
import sys
from typing import List, Callable

from omoide import core
from omoide.use_cases import cli
from omoide.use_cases import commands
from omoide.use_cases.unite import unite


def main(args: List[str], *,
         filesystem: core.Filesystem = core.Filesystem(),
         stdout: core.STDOut = core.STDOut()) -> None:
    """Entry point."""
    if not args:
        stdout.yellow('No arguments to unite')
        return

    source_path = os.environ.get('OMOIDE_SOURCE')
    content_path = os.environ.get('OMOIDE_CONTENT')

    domain, command = cli.parse_arguments(args, source_path, content_path)

    if not filesystem.exists(command.sources_folder):
        raise FileNotFoundError(
            f'Sources folder {command.sources_folder} does not exist'
        )

    if not filesystem.exists(command.content_folder):
        filesystem.ensure_folder_exists(command.content_folder, stdout)

    target_func = get_target_func(domain)
    target_func(command, filesystem, stdout)


def get_target_func(domain: str) -> Callable:
    """Return perform func based on domain."""
    target_func = {
        'unite': perform_unite,
        'make_migrations': perform_make_migrations,
        'make_relocations': perform_make_relocations,
        'migrate': perform_migrate,
        'relocate': perform_relocate,
        'sync': perform_sync,
        'freeze': perform_freeze,
        'runserver': perform_runserver,
    }[domain]

    return target_func


def perform_unite(command: commands.UniteCommand,
                  filesystem: core.Filesystem,
                  stdout: core.STDOut) -> None:
    """Perform unite command."""
    stdout.print('Parsing source files')
    total = unite.act(command, filesystem, stdout)
    stdout.print(f'Total {total} units created')


def perform_make_migrations(command: commands.MakeMigrationsCommand,
                            filesystem: core.Filesystem,
                            stdout: core.STDOut) -> None:
    """Perform unite command."""
    stdout.print('Making migrations')
    # TODO


def perform_make_relocations(command: commands.MakeRelocationsCommand,
                             filesystem: core.Filesystem,
                             stdout: core.STDOut) -> None:
    """Perform make_relocations command."""
    stdout.print('Making relocations')
    # TODO


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
