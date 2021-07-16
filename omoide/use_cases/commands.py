# -*- coding: utf-8 -*-

"""Data transfer objects for command line operations.
"""
from dataclasses import dataclass

from typing import Union

__all__ = [
    'UniteCommand',
    'MakeRelocationsCommand',
    'MakeMigrationsCommand',
    'MigrateCommand',
    'RelocateCommand',
    'SyncCommand',
    'FreezeCommand',
    'RunserverCommand',
    'AnyPathCommand',
    'AnyCommand',
]


@dataclass(frozen=True)
class BaseCommand:
    """Knows only basic things."""
    sources_folder: str
    storage_folder: str
    content_folder: str
    branch: str
    leaf: str
    name: str


@dataclass(frozen=True)
class UniteCommand(BaseCommand):
    """We have nothing ready, lets create base unit of source information."""
    name: str = 'step_01_unite'


@dataclass(frozen=True)
class MakeRelocationsCommand(BaseCommand):
    """We have parsed source file, lets create some relocation files."""
    name: str = 'make_relocations'


@dataclass(frozen=True)
class MakeMigrationsCommand(BaseCommand):
    """We have parsed source file, lets create some migration files."""
    name: str = 'make_migrations'


@dataclass(frozen=True)
class MigrateCommand(BaseCommand):
    """We have migrations, lets apply them to leaf databases."""
    name: str = 'migrate'


@dataclass(frozen=True)
class RelocateCommand(BaseCommand):
    """Move and compress actual media content."""
    name: str = 'relocate'


@dataclass(frozen=True)
class SyncCommand(BaseCommand):
    """We have filled leaf databases, lets gather information into root."""
    name: str = 'sync'


@dataclass(frozen=True)
class FreezeCommand(BaseCommand):
    """Create static database."""
    name: str = 'freeze'


@dataclass(frozen=True)
class RunserverCommand:
    """Start web application."""
    host: str = ''
    port: int = ''
    template_folder: str = ''
    static_folder: str = ''
    name: str = 'runserver'


AnyPathCommand = Union[
    UniteCommand,
    MakeRelocationsCommand,
    MakeMigrationsCommand,
    MigrateCommand,
    RelocateCommand,
    SyncCommand,
    FreezeCommand,
]

AnyCommand = Union[
    UniteCommand,
    MakeRelocationsCommand,
    MakeMigrationsCommand,
    MigrateCommand,
    RelocateCommand,
    SyncCommand,
    FreezeCommand,
    RunserverCommand
]
