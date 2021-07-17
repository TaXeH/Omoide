# -*- coding: utf-8 -*-

"""Tools required to generate unique identifiers.
"""
from itertools import chain

from omoide import constants
from omoide import core
from omoide import use_cases
from omoide.use_cases.unite.class_identity_master import IdentityMaster
from omoide.use_cases.unite.class_router import Router
from omoide.use_cases.unite.class_uuid_master import UUIDMaster


def gather_existing_identities(storage_folder: str,
                               router: Router,
                               identity_master: IdentityMaster,
                               uuid_master: UUIDMaster,
                               filesystem: core.Filesystem) -> None:
    """Get all variables and all UUID from existing files."""
    walk = use_cases.utils.walk(storage_folder, filesystem)

    for branch, leaf, leaf_folder in walk:
        unit_file_path = filesystem.join(leaf_folder, constants.UNIT_FILE_NAME)

        if filesystem.not_exists(unit_file_path):
            continue

        raw_unit = filesystem.read_json(unit_file_path)

        gather_routes_from_unit(raw_unit, router)
        gather_variables_from_unit(raw_unit, identity_master)
        gather_uuids_from_unit(raw_unit, uuid_master)


def gather_routes_from_unit(raw_unit: dict, router: Router) -> None:
    """Find all routes in given unit and store them into router."""
    objects = chain(
        raw_unit.get('realms', []),
        raw_unit.get('themes', []),
        raw_unit.get('groups', []),
    )

    for each in objects:
        router.register_route(each['uuid'], each['route'])


def gather_uuids_from_unit(raw_unit: dict,
                           uuid_master: UUIDMaster) -> None:
    """Find all UUIDs in given unit and store them into UUID master."""
    for fields in raw_unit.get('variables', {}).values():
        for value in fields.values():
            uuid_master.add_existing_uuid(value)


def gather_variables_from_unit(raw_unit: dict,
                               identity_master: IdentityMaster
                               ) -> None:
    """Find all variables in given unit and store them into Identity master."""
    for fields in raw_unit.get('variables', {}).values():
        for variable, value in fields.items():
            identity_master.add_variable(variable, value)
