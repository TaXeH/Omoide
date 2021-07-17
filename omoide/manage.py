# -*- coding: utf-8 -*-

"""Main control tool.

Possible call variants:

    To analyze source files and create unit files:
        python manage.py unite all all
        python manage.py unite source_folder_1
        python manage.py unite source_folder_1 all
        python manage.py unite source_folder_1 leaf_folder_1

    To make migrations:
        python manage.py make_migrations all all
        python manage.py make_migrations source_folder_1
        python manage.py make_migrations source_folder_1 all
        python manage.py make_migrations source_folder_1 leaf_folder_1

    To make relocations:
        python manage.py make_relocations all all
        python manage.py make_relocations source_folder_1
        python manage.py make_relocations source_folder_1 all
        python manage.py make_relocations source_folder_1 leaf_folder_1

    To perform migrations:
        python manage.py migrate all all
        python manage.py migrate source_folder_1
        python manage.py migrate source_folder_1 all
        python manage.py migrate source_folder_1 leaf_folder_1

    To relocate and resize media files:
        python manage.py relocate all all
        python manage.py relocate source_folder_1
        python manage.py relocate source_folder_1 all
        python manage.py relocate source_folder_1 leaf_folder_1

    To synchronize databases:
        python manage.py sync all all
        python manage.py sync branch source_folder_1
        python manage.py sync leaf leaf_folder_1

    To create final static database:
        python manage.py freeze

    To launch development server:
        python manage.py runserver
        python manage.py runserver 9000
        python manage.py runserver 127.0.0.1:9000

    For all commands:
        Use --sources to specify sources folder.
        Use --storage to specify storage folder.
        Use --content to specify content folder.
"""
import os
import sys
from typing import List, Callable, Optional

from omoide import core, use_cases
from omoide.use_cases import cli
from omoide.use_cases import commands


def main(args: List[str], *,
         filesystem: core.Filesystem = core.Filesystem(),
         stdout: core.STDOut = core.STDOut()) -> None:
    """Entry point."""
    if not args:
        stdout.yellow('No arguments to handle')
        return

    sources_path = get_and_announce('OMOIDE_SOURCE', stdout)
    storage_path = get_and_announce('OMOIDE_STORAGE', stdout)
    content_path = get_and_announce('OMOIDE_CONTENT', stdout)

    command = cli.parse_arguments(args, sources_path,
                                  storage_path, content_path)

    if command.sources_folder \
            and filesystem.not_exists(command.sources_folder):
        raise FileNotFoundError(
            f'Sources folder does not exist: {command.sources_folder}'
        )

    if command.storage_folder \
            and filesystem.not_exists(command.storage_folder):
        filesystem.ensure_folder_exists(command.content_folder, stdout)

    if command.content_folder \
            and filesystem.not_exists(command.content_folder):
        filesystem.ensure_folder_exists(command.content_folder, stdout)

    target_func = get_target_func(command)
    target_func(command, filesystem, stdout)


def get_and_announce(variable: str, stdout: core.STDOut) -> Optional[str]:
    """Notice that variable is not None."""
    value = os.environ.get(variable)
    if value is not None:
        stdout.yellow(f'Using {variable}={value!r}')
    return value


def get_target_func(command: use_cases.AnyCommand) -> Callable:
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
    }[command.name]

    return target_func


def perform_unite(command: commands.UniteCommand,
                  filesystem: core.Filesystem,
                  stdout: core.STDOut) -> None:
    """Perform unite command."""
    stdout.magenta('[UNITE] Parsing source files and making unit files')
    total = use_cases.unite.act(command, filesystem, stdout)
    stdout.magenta(f'Total {total} unit files created')


def perform_make_migrations(command: commands.MakeMigrationsCommand,
                            filesystem: core.Filesystem,
                            stdout: core.STDOut) -> None:
    """Perform unite command."""
    stdout.magenta('[MAKE MIGRATIONS] Creating migration files')
    total = use_cases.make_migrations.act(command, filesystem, stdout)
    stdout.magenta(f'Total {total} migration operations created')


def perform_make_relocations(command: commands.MakeRelocationsCommand,
                             filesystem: core.Filesystem,
                             stdout: core.STDOut) -> None:
    """Perform make_relocations command."""
    stdout.magenta('[MAKE RELOCATIONS] Creating relocation files')
    total = use_cases.make_relocations.act(command, filesystem, stdout)
    stdout.magenta(f'Total {total} relocation operations created')


def perform_migrate(command: commands.MigrateCommand,
                    filesystem: core.Filesystem,
                    stdout: core.STDOut) -> None:
    """Perform migration command."""
    stdout.magenta('[MIGRATE] Applying migrations')
    total = use_cases.migrate.act(command, filesystem, stdout)
    stdout.magenta(f'Total {total} migration operations applied')


def perform_relocate(command: commands.RelocateCommand,
                     filesystem: core.Filesystem,
                     stdout: core.STDOut) -> None:
    """Perform relocation command."""
    stdout.magenta('[RELOCATE] Applying relocations')
    total = use_cases.relocate.act(command, filesystem, stdout)
    stdout.magenta(f'Total {total} relocation operations applied')


def perform_sync(command: commands.SyncCommand,
                 filesystem: core.Filesystem,
                 stdout: core.STDOut) -> None:
    """Perform sync command."""
    stdout.magenta('[SYNC] Synchronizing databases')
    total = use_cases.sync.act(command, filesystem, stdout)
    stdout.magenta(f'Total {total} databases synchronized')


def perform_freeze(command: commands.FreezeCommand,
                   filesystem: core.Filesystem,
                   stdout: core.STDOut) -> None:
    """Perform freeze command."""
    stdout.magenta('[FREEZE] Making static database')
    # TODO
    raise


def perform_runserver(command: commands.RunserverCommand,
                      filesystem: core.Filesystem,
                      stdout: core.STDOut) -> None:
    """Perform command."""
    stdout.magenta('[RUNSERVER] Starting server')
    # TODO
    raise


if __name__ == '__main__':
    main(sys.argv[1:])
