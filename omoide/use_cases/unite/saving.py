# -*- coding: utf-8 -*-

"""Filesystem tools.
"""
from dataclasses import asdict
from typing import List

from omoide import constants
from omoide import core
from omoide.core.transfer_objects import Relocation, SQL


def save_migrations(leaf_folder: str, migrations: List[SQL],
                    filesystem: core.Filesystem) -> str:
    """Save migration as SQL file."""
    file_path = filesystem.join(leaf_folder, constants.MIGRATION_FILE_NAME)
    filesystem.write_file(file_path, ';\n'.join(map(str, migrations)))
    return file_path


def save_relocations(leaf_folder: str,
                     relocations: List[Relocation],
                     filesystem: core.Filesystem) -> str:
    """Save relocations as JSON file."""
    file_path = filesystem.join(leaf_folder, constants.RELOCATION_FILE_NAME)
    filesystem.write_json(file_path, [asdict(x) for x in relocations])
    return file_path
