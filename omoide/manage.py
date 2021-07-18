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

    To display folder structure:
        python manage.py show_tree

    For all commands:
        Use --sources to specify sources folder.
        Use --storage to specify storage folder.
        Use --content to specify content folder.
"""
import os
import sys
from typing import List, Callable, Optional

from omoide import commands
from omoide import rite
from omoide import incarnation


def main(args: List[str],
         *,
         filesystem: rite.Filesystem = rite.Filesystem(),
         stdout: rite.STDOut = rite.STDOut()) -> None:
    """Entry point."""
    if not args:
        stdout.yellow('No arguments to handle')
        return

    sources_path = get_and_announce('OMOIDE_SOURCE', stdout)
    storage_path = get_and_announce('OMOIDE_STORAGE', stdout)
    content_path = get_and_announce('OMOIDE_CONTENT', stdout)

    command = commands.parse_arguments(args, sources_path,
                                       storage_path, content_path)

    if isinstance(command, commands.FilesRelatedCommand):
        assert_sources_folder_exist(command, filesystem, stdout)
        filesystem.ensure_folder_exists(command.storage_folder, stdout)
        filesystem.ensure_folder_exists(command.content_folder, stdout)
        command.sources_folder = filesystem.absolute(command.sources_folder)
        command.storage_folder = filesystem.absolute(command.storage_folder)
        command.content_folder = filesystem.absolute(command.content_folder)

    elif getattr(command, 'name') == 'runserver':
        command.content_folder = filesystem.absolute(command.content_folder)
        command.template_folder = filesystem.absolute(command.template_folder)
        command.static_folder = filesystem.absolute(command.static_folder)

    target_func = get_target_func(command)
    target_func(command, filesystem, stdout)


def assert_sources_folder_exist(command: commands.FilesRelatedCommand,
                                filesystem: rite.Filesystem,
                                stdout: rite.STDOut) -> None:
    """Stop execution if source folder does not exist."""
    if filesystem.not_exists(command.sources_folder):
        stdout.red(f'Sources folder does not exist: {command.sources_folder}')
        sys.exit(1)


def get_and_announce(variable: str, stdout: rite.STDOut) -> Optional[str]:
    """Announce that variable is not None."""
    value = os.environ.get(variable)
    if value is not None:
        stdout.yellow(f'Using {variable}={value!r}')
    return value


def get_target_func(command: commands.BaseCommand) -> Callable:
    """Return perform func based on domain."""
    target_func = {
        'unite': perform_unite,
        'make_migrations': perform_make_migrations,
        'make_relocations': perform_make_relocations,
        'migrate': perform_migrate,
        'relocate': perform_relocate,
        'sync': perform_sync,
        'freeze': perform_freeze,
        'show_tree': perform_show_tree,
        'runserver': perform_runserver,
    }[getattr(command, 'name')]

    return target_func


def perform_unite(command: commands.UniteCommand,
                  filesystem: rite.Filesystem,
                  stdout: rite.STDOut) -> None:
    """Perform unite command."""
    stdout.magenta('[UNITE] Parsing source files and making unit files')
    total = incarnation.act_unite(command, filesystem, stdout)
    stdout.magenta(f'Total {total} unit files created')


def perform_make_migrations(command: commands.MakeMigrationsCommand,
                            filesystem: rite.Filesystem,
                            stdout: rite.STDOut) -> None:
    """Perform unite command."""
    stdout.magenta('[MAKE MIGRATIONS] Creating migration files')
    total = incarnation.act_make_migrations(command, filesystem, stdout)
    stdout.magenta(f'Total {total} migration operations created')


def perform_make_relocations(command: commands.MakeRelocationsCommand,
                             filesystem: rite.Filesystem,
                             stdout: rite.STDOut) -> None:
    """Perform make_relocations command."""
    stdout.magenta('[MAKE RELOCATIONS] Creating relocation files')
    total = incarnation.act_make_relocations(command, filesystem, stdout)
    stdout.magenta(f'Total {total} relocation operations created')


def perform_migrate(command: commands.MigrateCommand,
                    filesystem: rite.Filesystem,
                    stdout: rite.STDOut) -> None:
    """Perform migration command."""
    stdout.magenta('[MIGRATE] Applying migrations')
    total = incarnation.act_migrate(command, filesystem, stdout)
    stdout.magenta(f'Total {total} migration operations applied')


def perform_relocate(command: commands.RelocateCommand,
                     filesystem: rite.Filesystem,
                     stdout: rite.STDOut) -> None:
    """Perform relocation command."""
    stdout.magenta('[RELOCATE] Applying relocations')
    total = incarnation.act_relocate(command, filesystem, stdout)
    stdout.magenta(f'Total {total} relocation operations applied')


def perform_sync(command: commands.SyncCommand,
                 filesystem: rite.Filesystem,
                 stdout: rite.STDOut) -> None:
    """Perform sync command."""
    stdout.magenta('[SYNC] Synchronizing databases')
    total = incarnation.act_sync(command, filesystem, stdout)
    stdout.magenta(f'Total {total} databases synchronized')


def perform_freeze(command: commands.FreezeCommand,
                   filesystem: rite.Filesystem,
                   stdout: rite.STDOut) -> None:
    """Perform freeze command."""
    stdout.magenta('[FREEZE] Making static database')
    incarnation.act_freeze(command, filesystem, stdout)
    stdout.magenta(f'Successfully created static database')


def perform_runserver(command: commands.RunserverCommand,
                      filesystem: rite.Filesystem,
                      stdout: rite.STDOut) -> None:
    """Perform command."""
    stdout.magenta('[RUNSERVER] Starting server')
    command.content_folder = filesystem.absolute(command.content_folder)
    incarnation.act_runserver(command, filesystem, stdout)


def perform_show_tree(command: commands.ShowTreeCommand,
                      filesystem: rite.Filesystem,
                      stdout: rite.STDOut) -> None:
    """Perform command."""
    stdout.magenta('[SHOW_TREE] Displaying folder tree')
    total = incarnation.act_show_tree(command, filesystem, stdout)
    stdout.magenta(f'Got {total} subfolders')


if __name__ == '__main__':
    main(sys.argv[1:])
