# -*- coding: utf-8 -*-

"""Command line utils.
"""
from typing import List, Type, Optional, Tuple, TypeVar

from omoide.use_cases import commands
from omoide.use_cases import constants

T = TypeVar('T')


def parse_arguments(args: List[str],
                    sources_folder: Optional[str],
                    content_folder: Optional[str]):
    """Construct operation from arguments."""
    sources_folder, args = extract_parameter(
        name=constants.SOURCES_FOLDER_NAME,
        args=args,
        variant=sources_folder,
        default=constants.DEFAULT_SOURCES_FOLDER,
    )

    content_folder, args = extract_parameter(
        name=constants.CONTENT_FOLDER_NAME,
        args=args,
        variant=content_folder,
        default=constants.DEFAULT_CONTENT_FOLDER
    )

    args = [x.lower() for x in args]
    command, rest = args[0], args[1:]

    if command == 'make_migrations':
        operation = make_operation_migrations(rest,
                                              sources_folder, content_folder)

    elif command == 'migrate':
        operation = make_operation_migrate(rest,
                                           sources_folder, content_folder)

    elif command == 'sync':
        operation = make_operation_sync(rest,
                                        sources_folder, content_folder)

    elif command == 'freeze':
        operation = make_operation_freeze(sources_folder, content_folder)

    elif command == 'runserver':
        operation = make_operation_runserver(rest, content_folder)

    else:
        raise ValueError(f'Unknown command: {command}')

    return operation


def extract_parameter(name: str, args: List[str],
                      variant: Optional[str] = None,
                      default: Optional[str] = '.') -> Tuple[str, List[str]]:
    """Try extracting parameter from arguments."""
    key = f'--{name}'
    for i, value in enumerate(args):
        if value == key:
            if i >= len(args) - 1:
                raise ValueError(
                    f'You need to specify value for {key} parameter'
                )
            result = args[i + 1]
            resulting_args = args[:i] + args[i + 2:]
            break

    else:
        result = variant or default
        resulting_args = args.copy()

    return result, resulting_args


def extract_flag(name: str, args: List[str],
                 default: bool) -> Tuple[bool, List[str]]:
    """Try extracting flag from arguments."""
    key = f'--{name}'
    for i, value in enumerate(args):
        if value == key:
            result = True
            resulting_args = args[:i] + args[i + 1:]
            break

    else:
        result = default
        resulting_args = args.copy()

    return result, resulting_args


def make_operation_migrations(args: List[str],
                              source_folder: str,
                              content_folder: str
                              ) -> commands.MakeMigrationsCommand:
    """Make migration preparation operation."""
    return _make_operation_base_migration(args,
                                          commands.MakeMigrationsCommand,
                                          source_folder,
                                          content_folder)


def make_operation_migrate(args: List[str],
                           source_folder: str,
                           content_folder: str
                           ) -> commands.MigrateCommand:
    """Make migration operation."""
    return _make_operation_base_migration(args,
                                          commands.MigrateCommand,
                                          source_folder,
                                          content_folder)


def _make_operation_base_migration(args: List[str],
                                   desired_type: Type[T],
                                   source_folder: str,
                                   content_folder: str) -> T:
    """Common creation of migration operation."""
    trunk = 'all'
    leaf = 'all'

    if len(args) == 1:
        trunk = args[0]

    elif len(args) >= 2:
        trunk, leaf, *_ = args

    if trunk == 'all' and leaf != 'all':
        raise ValueError(
            f'You cannot use all trunks with specific leaf (given {leaf})'
        )

    return desired_type(trunk=trunk,
                        leaf=leaf,
                        sources_folder=source_folder,
                        content_folder=content_folder)


def make_operation_sync(args: List[str], source_folder: str,
                        content_folder: str) -> commands.SyncCommand:
    """Make sync operation."""
    nocopy, args = extract_flag('nocopy', args, default=False)
    trunk = 'all'
    leaf = 'all'

    if len(args) == 0:
        pass

    elif len(args) == 1:
        raise ValueError(
            'To perform sync you need to supply '
            'target (trunk or leaf) and a folder name'
        )

    elif len(args) >= 2:
        target, folder, *_ = args
        if target == 'trunk':
            trunk = folder
            leaf = 'all'

        elif target == 'leaf':
            trunk = 'find'
            leaf = folder

        else:
            raise ValueError(f'Unknown sync target {target}')

    return commands.SyncCommand(trunk=trunk,
                                leaf=leaf,
                                sources_folder=source_folder,
                                content_folder=content_folder)


def make_operation_freeze(source_folder: str,
                          content_folder: str) -> commands.FreezeCommand:
    """Make freeze operation."""
    return commands.FreezeCommand(sources_folder=source_folder,
                                  content_folder=content_folder)


def make_operation_runserver(args: List[str],
                             content_folder: str) -> commands.RunserverCommand:
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

    return commands.RunserverCommand(host=host,
                                     port=port,
                                     content_folder=content_folder)
