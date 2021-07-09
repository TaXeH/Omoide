from dataclasses import asdict
from typing import List

from omoide import core, constants
from omoide.core import Relocation


def save_relocations(folder: str,
                     relocations: List[Relocation],
                     filesystem: core.Filesystem) -> str:
    """Save relocations as JSON file."""
    file_path = filesystem.join(folder, constants.RELOCATION_FILE_NAME)
    filesystem.write_json(file_path, [asdict(x) for x in relocations])
    return file_path
