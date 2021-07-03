from typing import List, Tuple, Dict

from omoide import core
from omoide.database import operations as db_operations, utils as db_utils


def make_global_uuid_master(paths_to_databases: List[Tuple[str, str]],
                            aliases: Dict[str, str],
                            filesystem: core.Filesystem,
                            stdout: core.STDOut) -> core.UUIDMaster:
    """Create instance of UUIDMater that knows all databases."""
    main_uuid_master = core.UUIDMaster()

    for folder, file in paths_to_databases:
        path = filesystem.join(folder, file)
        if filesystem.not_exists(path):
            stdout.yellow(f'Database does not exist: {path}')
            continue

        database = db_operations.create_database(
            folder=folder,
            filename=file,
            filesystem=filesystem,
            stdout=stdout,
            echo=True,
        )

        uuid_master = db_utils.create_uuid_mater_from_db(database, aliases)
        main_uuid_master += uuid_master

    return main_uuid_master