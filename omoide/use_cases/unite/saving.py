# -*- coding: utf-8 -*-

"""Filesystem tools.
"""
from typing import List

import omoide.files.constants
from omoide import core
from omoide.use_cases.make_relocations.class_relocation import Relocation
from omoide.use_cases.make_migrations.class_sql import SQL


def save_migrations(leaf_folder: str, migrations: List[SQL],
                    filesystem: core.Filesystem) -> str:
    """Save migration as SQL file."""
    file_path = filesystem.join(
        leaf_folder,
        omoide.files.constants.MIGRATION_FILENAME,
    )

    filesystem.write_file(file_path, ';\n'.join(map(str, migrations)))

    return file_path


def save_relocations(leaf_folder: str,
                     relocations: List[Relocation],
                     filesystem: core.Filesystem) -> str:
    """Save relocations as JSON file."""
    file_path = filesystem.join(
        leaf_folder,
        omoide.files.constants.RELOCATION_FILENAME,
    )

    filesystem.write_json(file_path, [x.as_json() for x in relocations])

    return file_path
