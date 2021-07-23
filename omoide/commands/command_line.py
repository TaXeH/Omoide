# -*- coding: utf-8 -*-

"""Command line utils.
"""
from functools import partial
from typing import List, Type, Optional, Tuple, TypeVar

from omoide import constants
from omoide.commands import instances

__all__ = [
    'parse_arguments',
    'extract_parameter',
    'make_operation_runserver',
]


def parse_arguments(args: List[str]) -> instances.BaseCommand:
    """Construct operation from arguments."""
    sources_folder, args = extract_parameter(
        name=constants.SOURCES_FOLDER_NAME,
        args=args,
        default=constants.DEFAULT_SOURCES_FOLDER,
    )

    storage_folder, args = extract_parameter(
        name=constants.STORAGE_FOLDER_NAME,
        args=args,
        default=constants.DEFAULT_STORAGE_FOLDER,
    )

    content_folder, args = extract_parameter(
        name=constants.CONTENT_FOLDER_NAME,
        args=args,
        default=constants.DEFAULT_CONTENT_FOLDER,
    )

    database_folder, args = extract_parameter(
        name=constants.DATABASE_FOLDER_NAME,
        args=args,
        default=constants.DEFAULT_DATABASE_FOLDER,
    )

    force, args = extract_flag('force', args, default=False)

    args = [x.lower() for x in args]
    command, rest = args[0], args[1:]

    maker = partial(_make_common,
                    sources_folder=sources_folder,
                    storage_folder=storage_folder,
                    content_folder=content_folder,
                    database_folder=database_folder,
                    force=force)

    if command == 'unite':
        instance = maker(rest, instances.UniteCommand)

    elif command == 'make_migrations':
        instance = maker(rest, instances.MakeMigrationsCommand)

    elif command == 'make_relocations':
        instance = maker(rest, instances.MakeRelocationsCommand)

    elif command == 'migrate':
        instance = maker(rest, instances.MigrateCommand)

    elif command == 'relocate':
        instance = maker(rest, instances.RelocateCommand)

    elif command == 'sync':
        instance = maker(rest, instances.SyncCommand)

    elif command == 'freeze':
        instance = maker(rest, instances.FreezeCommand)

    elif command == 'show_tree':
        instance = maker(rest, instances.ShowTreeCommand)

    elif command == 'runserver':
        instance = make_operation_runserver(rest, database_folder)

    else:
        raise ValueError(f'Unknown command: {command!r}')

    return instance


def extract_parameter(name: str, args: List[str],
                      default: Optional[str] = '.') -> Tuple[str, List[str]]:
    """Try extracting parameter from arguments."""
    keys = [f'--{name}', f'-{name[0].lower()}']
    result = default
    resulting_args = args.copy()

    for i, value in enumerate(args):
        if value in keys:
            if i >= len(args) - 1:
                break
            result = args[i + 1]
            resulting_args = args[:i] + args[i + 2:]
            break

    return result, resulting_args


def extract_flag(name: str, args: List[str],
                 default: bool) -> Tuple[bool, List[str]]:
    """Try extracting flag from arguments."""
    keys = [f'--{name}', f'-{name[0].lower()}']
    for i, value in enumerate(args):
        if value in keys:
            result = True
            resulting_args = args[:i] + args[i + 1:]
            break

    else:
        result = default
        resulting_args = args.copy()

    return result, resulting_args


T = TypeVar('T')


def _make_common(args: List[str],
                 desired_type: Type[T],
                 sources_folder: str,
                 storage_folder: str,
                 content_folder: str,
                 database_folder: str,
                 force: bool) -> T:
    """Common creation of operation."""
    if len(args) == 0:
        branch, leaf = 'all', 'all'

    elif len(args) == 1:
        branch, leaf = args[0], 'all'

    else:
        branch, leaf, *_ = args

    return desired_type(branch=branch,
                        leaf=leaf,
                        sources_folder=sources_folder,
                        storage_folder=storage_folder,
                        content_folder=content_folder,
                        database_folder=database_folder,
                        force=force)


def make_operation_runserver(args: List[str], database_folder: str
                             ) -> instances.RunserverCommand:
    """Make server running operation."""
    host = constants.DEFAULT_SERVER_HOST
    port = constants.DEFAULT_SERVER_PORT

    if args:
        command = args[0]
        parts = command.strip().split(':')
        given_port = str(port)
        given_host = ''

        if len(parts) == 1:
            given_port = parts[0]

        elif len(parts) >= 2:
            given_host, given_port, *_ = parts

        if given_port.isnumeric():
            port = int(given_port)
        else:
            raise ValueError(f'Wrong port for server {given_port}')

        host = given_host or host

    return instances.RunserverCommand(
        host=host,
        port=port,
        database_folder=database_folder,
        template_folder=constants.DEFAULT_TEMPLATE_FOLDER,
        static_folder=constants.DEFAULT_STATIC_FOLDER,
    )
