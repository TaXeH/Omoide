from typing import List

from omoide import core, constants
from omoide.core import SQL


def save_migrations(leaf_folder: str, migrations: List[SQL],
                    filesystem: core.Filesystem) -> str:
    """Save migration as SQL file."""
    file_path = filesystem.join(leaf_folder, constants.MIGRATION_FILE_NAME)
    filesystem.write_file(file_path, ';\n'.join(map(str, migrations)))
    return file_path
