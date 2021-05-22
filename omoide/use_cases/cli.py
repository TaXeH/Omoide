# -*- coding: utf-8 -*-

"""Command line utils.
"""
from dataclasses import dataclass
from typing import List, Type, TypeVar, Optional, Tuple

import omoide.use_cases.constants
from omoide.use_cases import constants


@dataclass(frozen=True)
class BuildCommand:
    """Create static database."""
    sources_path: str
    content_path: str


@dataclass(frozen=True)
class MakeMigrationCommand:
    """Migration creation operation setup."""
    trunk: str
    leaf: str
    sources_path: str
    content_path: str


@dataclass(frozen=True)
class MigrateCommand:
    """Migration operation setup."""
    trunk: str
    leaf: str
    sources_path: str
    content_path: str


TMig = TypeVar('TMig', MakeMigrationCommand, MigrateCommand)


@dataclass(frozen=True)
class SyncCommand:
    """Sync operation setup."""
    trunk: str
    leaf: str
    sources_path: str
    content_path: str
    nocopy: bool


@dataclass(frozen=True)
class RunserverCommand:
    """Server startup operation setup."""
    host: str
    port: int
    content_path: str


def parse_arguments(args: List[str],
                    sources_path: Optional[str],
                    content_path: Optional[str]):
    """Construct operation from arguments."""
    sources_path, args = extract_parameter(
        name=constants.SOURCES_FOLDER_NAME,
        args=args,
        variant=sources_path,
        default=constants.DEFAULT_SOURCES_FOLDER,
    )

    content_path, args = extract_parameter(
        name=constants.CONTENT_FOLDER_NAME,
        args=args,
        variant=content_path,
        default=constants.DEFAULT_CONTENT_FOLDER
    )

    args = [x.lower() for x in args]
    command, rest = args[0], args[1:]

    if command == 'makemigrations':
        operation = make_operation_migrations(rest, sources_path, content_path)

    elif command == 'migrate':
        operation = make_operation_migrate(rest, sources_path, content_path)

    elif command == 'sync':
        operation = make_operation_sync(rest, sources_path, content_path)

    elif command == 'runserver':
        operation = make_operation_runserver(rest, content_path)

    else:
        raise ValueError(f'Unknown command {command}')

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


def make_operation_migrations(args: List[str], source_path: str,
                              content_path: str) -> MakeMigrationCommand:
    """Make migration preparation operation."""
    return _make_operation_base_migration(args, MakeMigrationCommand,
                                          source_path, content_path)


def make_operation_migrate(args: List[str], source_path: str,
                           content_path: str) -> MigrateCommand:
    """Make migration operation."""
    return _make_operation_base_migration(args, MigrateCommand,
                                          source_path, content_path)


def _make_operation_base_migration(args: List[str],
                                   desired_type: Type[TMig],
                                   source_path: str,
                                   content_path: str) -> TMig:
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

    return desired_type(
        trunk=trunk,
        leaf=leaf,
        sources_path=source_path,
        content_path=content_path,
    )


def make_operation_sync(args: List[str], source_path: str,
                        content_path: str) -> SyncCommand:
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

    return SyncCommand(
        trunk=trunk,
        leaf=leaf,
        sources_path=source_path,
        content_path=content_path,
        nocopy=nocopy,
    )


def make_operation_runserver(args: List[str],
                             content_path: str) -> RunserverCommand:
    """Make server running operation."""
    host = omoide.use_cases.constants.DEFAULT_SERVER_HOST
    port = omoide.use_cases.constants.DEFAULT_SERVER_PORT

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

    return RunserverCommand(
        host=host,
        port=port,
        content_path=content_path,
    )
