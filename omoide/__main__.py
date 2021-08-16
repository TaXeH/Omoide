# -*- coding: utf-8 -*-

"""Main control tool.

Possible call variants:

    To analyze source files and create unit files:
        python -m omoide unite all all
        python -m omoide unite source_folder_1
        python -m omoide unite source_folder_1 all
        python -m omoide unite source_folder_1 leaf_folder_1

    To make migrations:
        python -m omoide make_migrations all all
        python -m omoide make_migrations source_folder_1
        python -m omoide make_migrations source_folder_1 all
        python -m omoide make_migrations source_folder_1 leaf_folder_1

    To make relocations:
        python -m omoide make_relocations all all
        python -m omoide make_relocations source_folder_1
        python -m omoide make_relocations source_folder_1 all
        python -m omoide make_relocations source_folder_1 leaf_folder_1

    To perform migrations:
        python -m omoide migrate all all
        python -m omoide migrate source_folder_1
        python -m omoide migrate source_folder_1 all
        python -m omoide migrate source_folder_1 leaf_folder_1

    To relocate and resize media files:
        python -m omoide relocate all all
        python -m omoide relocate source_folder_1
        python -m omoide relocate source_folder_1 all
        python -m omoide relocate source_folder_1 leaf_folder_1

    To synchronize databases:
        python -m omoide sync all all
        python -m omoide sync branch source_folder_1
        python -m omoide sync leaf leaf_folder_1

    To create final static database:
        python -m omoide freeze

    To launch development server:
        python -m omoide runserver
        python -m omoide runserver 9000
        python -m omoide runserver 127.0.0.1:9000

        Use --reload to turn on auto reload.

    To display folder structure:
        python -m omoide show_tree

    For all commands:
        Use --sources to specify sources folder.
        Use --storage to specify storage folder.
        Use --content to specify content folder.
        Use --force to allow overwriting.
"""
import sys
from typing import List, Callable

from omoide import commands
from omoide import infra
from omoide.commands import perform


def main(args: List[str],
         *,
         filesystem: infra.Filesystem = infra.Filesystem(),
         stdout: infra.STDOut = infra.STDOut()) -> None:
    """Entry point."""
    if not args:
        stdout.yellow('No arguments to handle')
        return

    command = commands.parse_arguments(args)

    if isinstance(command, commands.FilesRelatedCommand):
        assert_sources_folder_exist(command, filesystem, stdout)
        filesystem.ensure_folder_exists(command.storage_folder, stdout)
        filesystem.ensure_folder_exists(command.content_folder, stdout)
        command.sources_folder = filesystem.absolute(command.sources_folder)
        command.storage_folder = filesystem.absolute(command.storage_folder)
        command.content_folder = filesystem.absolute(command.content_folder)

    elif getattr(command, 'name') == 'runserver':
        command.content_folder = filesystem.absolute(command.content_folder)
        command.database_folder = filesystem.absolute(command.database_folder)
        command.template_folder = filesystem.absolute(command.template_folder)
        command.static_folder = filesystem.absolute(command.static_folder)

    target_func = get_target_func(command)
    target_func(command, filesystem, stdout)


def assert_sources_folder_exist(command: commands.FilesRelatedCommand,
                                filesystem: infra.Filesystem,
                                stdout: infra.STDOut) -> None:
    """Stop execution if source folder does not exist."""
    if filesystem.not_exists(command.sources_folder):
        stdout.red(f'Sources folder does not exist: {command.sources_folder}')
        sys.exit(1)


def get_target_func(command: commands.BaseCommand) -> Callable:
    """Return perform func based on domain."""
    target_func = {
        'unite': perform.perform_unite,
        'make_migrations': perform.perform_make_migrations,
        'make_relocations': perform.perform_make_relocations,
        'migrate': perform.perform_migrate,
        'relocate': perform.perform_relocate,
        'sync': perform.perform_sync,
        'freeze': perform.perform_freeze,
        'show_tree': perform.perform_show_tree,
        'runserver': perform.perform_runserver,
    }[getattr(command, 'name')]

    return target_func


if __name__ == '__main__':
    main(sys.argv[1:])
