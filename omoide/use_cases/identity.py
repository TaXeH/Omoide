# -*- coding: utf-8 -*-

"""Tools required to generate unique identifiers.
"""
from itertools import chain

from omoide import constants
from omoide import core
from omoide import use_cases


def gather_existing_identities(storage_folder: str,
                               router: use_cases.Router,
                               identity_master: use_cases.IdentityMaster,
                               uuid_master: use_cases.UUIDMaster,
                               filesystem: core.Filesystem) -> None:
    """Get all variables and all UUID from existing files."""
    walk = use_cases.utils.walk(storage_folder, filesystem)

    for branch, leaf, leaf_folder in walk:
        unit_file_path = filesystem.join(leaf_folder, constants.UNIT_FILE_NAME)

        if filesystem.not_exists(unit_file_path):
            continue

        unit = filesystem.read_json(unit_file_path)

        gather_routes_from_unit(unit, router)
        gather_variables_from_unit(unit, identity_master)

        uuids_file_path = filesystem.join(leaf_folder,
                                          constants.UUIDS_FILE_NAME)
        if filesystem.exists(uuids_file_path):
            uuids = filesystem.read_json(uuids_file_path)
            uuid_master.insert_queue(uuids)


def gather_routes_from_unit(unit: dict, router: use_cases.Router) -> None:
    """Find all routes in given unit and store them into router."""
    objects = chain(
        unit.get('realms', []),
        unit.get('themes', []),
        unit.get('groups', []),
    )

    for each in objects:
        router.register_route(each['uuid'], each['route'])


def gather_uuids_from_unit(unit: dict,
                           uuid_master: use_cases.UUIDMaster) -> None:
    """Find all UUIDs in given unit and store them into UUID master."""
    # print('gather_uuids_from_processed_source', content)
    # FIXME


def gather_variables_from_unit(unit: dict,
                               identity_master: use_cases.IdentityMaster
                               ) -> None:
    """Find all variables in given unit and store them into Identity master."""
    # print('gather_variables_from_processed_source', content)
    # FIXME
