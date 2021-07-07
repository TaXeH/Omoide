# -*- coding: utf-8 -*-

"""Data transfer objects for command line operations.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseCommand:
    """Knows only basic things."""
    branch: str
    leaf: str
    sources_folder: str
    content_folder: str


@dataclass(frozen=True)
class UniteCommand(BaseCommand):
    """We have nothing ready, lets create base unit of source information."""


@dataclass(frozen=True)
class MakeRelocationsCommand(BaseCommand):
    """We have parsed source file, lets create some relocation files."""


@dataclass(frozen=True)
class MakeMigrationsCommand(BaseCommand):
    """We have parsed source file, lets create some migration files."""


@dataclass(frozen=True)
class MigrateCommand(BaseCommand):
    """We have migrations, lets apply them to leaf databases."""


@dataclass(frozen=True)
class RelocateCommand(BaseCommand):
    """Move and compress actual media content."""


@dataclass(frozen=True)
class SyncCommand(BaseCommand):
    """We have filled leaf databases, lets gather information into root."""


@dataclass(frozen=True)
class FreezeCommand:
    """Create static database."""
    sources_folder: str
    content_folder: str


@dataclass(frozen=True)
class RunserverCommand:
    """Start web application."""
    host: str
    port: int
    content_folder: str
    template_folder: str = 'templates'
    static_folder: str = 'static'
