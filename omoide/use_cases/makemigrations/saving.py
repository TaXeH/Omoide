# -*- coding: utf-8 -*-

"""Filesystem tools.
"""
from typing import List

import omoide.files.constants
from omoide import core
from omoide.database import constants as db_constants
from omoide.use_cases.makemigrations.class_relocation import Relocation
from omoide.use_cases.makemigrations.class_sql import SQL


def save_sql_commands(source_folder: str, commands: List[SQL],
                      filesystem: core.Filesystem, stdout: core.STDOut):
    """Save migration as SQL file."""
    sub_path = filesystem.join(source_folder,
                               omoide.files.constants.MIGRATION_FILENAME)
    filesystem.write_file(sub_path, ';\n'.join(map(str, commands)))
    stdout.green(f'Wrote file: {sub_path}')


def save_relocations(source_folder: str,
                     relocations: List[Relocation],
                     filesystem: core.Filesystem,
                     stdout: core.STDOut) -> None:
    """Save relocations as JSON file."""
    sub_path = filesystem.join(source_folder, 'relocation.json')
    filesystem.write_json(sub_path, relocations)
    stdout.green(f'Wrote file: {sub_path}')
