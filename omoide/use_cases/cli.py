# -*- coding: utf-8 -*-

"""Command line utils.
"""
from typing import List, Type, Optional, Tuple, TypeVar

from omoide import constants
from omoide import use_cases

T = TypeVar('T')


def parse_arguments(args: List[str],
                    sources_folder: Optional[str],
                    storage_folder: Optional[str],
                    content_folder: Optional[str]) -> use_cases.AnyCommand:
    """Construct operation from arguments."""
    sources_folder, args = extract_parameter(
        name=constants.SOURCES_FOLDER_NAME,
        args=args,
        variant=sources_folder,
        default=constants.DEFAULT_SOURCES_FOLDER,
    )

    storage_folder, args = extract_parameter(
        name=constants.STORAGE_FOLDER_NAME,
        args=args,
        variant=storage_folder,
        default=constants.DEFAULT_STORAGE_FOLDER,
    )

    content_folder, args = extract_parameter(
        name=constants.CONTENT_FOLDER_NAME,
        args=args,
        variant=content_folder,
        default=constants.DEFAULT_CONTENT_FOLDER
    )

    args = [x.lower() for x in args]
    command, rest = args[0], args[1:]

    if command == 'unite':
        instance = make_operation_unite(rest,
                                        sources_folder,
                                        storage_folder,
                                        content_folder)
    elif command == 'make_migrations':
        instance = make_operation_migrations(rest,
                                             storage_folder,
                                             content_folder)
    elif command == 'make_relocations':
        instance = make_operation_relocations(rest,
                                              sources_folder,
                                              storage_folder,
                                              content_folder)
    elif command == 'migrate':
        instance = make_operation_migrate(rest,
                                          storage_folder,
                                          content_folder)
    elif command == 'relocate':
        instance = make_operation_relocate(rest,
                                           sources_folder,
                                           storage_folder,
                                           content_folder)
    elif command == 'sync':
        instance = make_operation_sync(rest, storage_folder, content_folder)

    elif command == 'freeze':
        instance = make_operation_freeze(storage_folder, content_folder)

    elif command == 'runserver':
        instance = make_operation_runserver(rest, content_folder)

    else:
        raise ValueError(f'Unknown command: {command}')

    return instance


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


def make_operation_unite(args: List[str],
                         source_folder: str,
                         storage_folder: str,
                         content_folder: str
                         ) -> use_cases.UniteCommand:
    """Make source processing operation."""
    return _make_common(args,
                        use_cases.UniteCommand,
                        source_folder,
                        storage_folder,
                        content_folder)


def make_operation_migrations(args: List[str],
                              storage_folder: str,
                              content_folder: str
                              ) -> use_cases.MakeMigrationsCommand:
    """Make migration preparation operation."""
    return _make_common(args, use_cases.MakeMigrationsCommand,
                        '', storage_folder, content_folder)


def make_operation_relocations(args: List[str],
                               sources_folder: str,
                               storage_folder: str,
                               content_folder: str
                               ) -> use_cases.MakeRelocationsCommand:
    """Make relocation preparation operation."""
    return _make_common(args, use_cases.MakeRelocationsCommand,
                        sources_folder, storage_folder, content_folder)


def make_operation_migrate(args: List[str],
                           storage_folder: str,
                           content_folder: str
                           ) -> use_cases.MigrateCommand:
    """Make migration operation."""
    return _make_common(args, use_cases.MigrateCommand,
                        '', storage_folder, content_folder)


def make_operation_relocate(args: List[str],
                            sources_folder: str,
                            storage_folder: str,
                            content_folder: str
                            ) -> use_cases.RelocateCommand:
    """Make relocation operation."""
    return _make_common(args, use_cases.RelocateCommand,
                        sources_folder, storage_folder, content_folder)


def make_operation_sync(args: List[str],
                        storage_folder: str,
                        content_folder: str) -> use_cases.SyncCommand:
    """Make sync operation."""
    return _make_common(args, use_cases.SyncCommand,
                        '', storage_folder, content_folder)


def _make_common(args: List[str],
                 desired_type: Type[T],
                 source_folder: str,
                 storage_folder: str,
                 content_folder: str) -> T:
    """Common creation of operation."""
    if len(args) != 2:
        raise ValueError(
            f'You must specify branch and leaf for operation'
        )

    branch, leaf = args

    return desired_type(branch=branch,
                        leaf=leaf,
                        sources_folder=source_folder,
                        storage_folder=storage_folder,
                        content_folder=content_folder)


def make_operation_freeze(storage_folder: str,
                          content_folder: str) -> use_cases.FreezeCommand:
    """Make freeze operation."""
    return use_cases.FreezeCommand(sources_folder='',
                                   storage_folder=storage_folder,
                                   content_folder=content_folder,
                                   branch='',
                                   leaf='')


def make_operation_runserver(args: List[str],
                             content_folder: str
                             ) -> use_cases.RunserverCommand:
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

    return use_cases.RunserverCommand(
        host=host,
        port=port,
        content_folder=content_folder,
        template_folder=constants.DEFAULT_TEMPLATE_FOLDER,
        static_folder=constants.DEFAULT_STATIC_FOLDER,
    )
