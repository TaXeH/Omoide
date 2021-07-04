# -*- coding: utf-8 -*-

"""Data transfer objects for command line operations.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class MakeMigrationsCommand:
    """We have nothing ready, lets create some migration files."""
    trunk: str
    leaf: str
    sources_folder: str
    content_folder: str


@dataclass(frozen=True)
class MigrateCommand:
    """We have migrations, lets apply them to leaf databases."""
    trunk: str
    leaf: str
    sources_folder: str
    content_folder: str


@dataclass(frozen=True)
class RelocateCommand:
    """Move and compress actual media content."""
    trunk: str
    leaf: str
    sources_folder: str
    content_folder: str


@dataclass(frozen=True)
class SyncCommand:
    """We have filled leaf databases, lets gather information into root."""
    trunk: str
    leaf: str
    sources_folder: str
    content_folder: str


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
