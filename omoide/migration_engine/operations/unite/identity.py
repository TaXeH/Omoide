# -*- coding: utf-8 -*-

"""Tools required to generate unique identifiers.
"""
from itertools import chain

from omoide import constants, infra
from omoide.migration_engine.operations import unite


def gather_existing_identities(storage_folder: str,
                               router: unite.Router,
                               identity_master: unite.IdentityMaster,
                               uuid_master: unite.UUIDMaster,
                               filesystem: infra.Filesystem) -> None:
    """Get all variables and all UUID from existing files."""
    for branch, leaf, leaf_folder in infra.walk(storage_folder, filesystem):

        unit_path = filesystem.join(leaf_folder, constants.UNIT_FILE_NAME)
        if filesystem.exists(unit_path):
            unit = filesystem.read_json(unit_path)
            gather_routes_from_unit(unit, router)

        cache_path = filesystem.join(leaf_folder, constants.CACHE_FILE_NAME)
        if filesystem.exists(cache_path):
            cache = filesystem.read_json(cache_path)
            gather_variables_from_cache(cache, identity_master)
            gather_uuids_from_cache(cache, uuid_master)


def gather_routes_from_unit(raw_unit: dict, router: unite.Router) -> None:
    """Find all routes in given unit and store them into router."""
    objects = chain(raw_unit.get('realms', []),
                    raw_unit.get('themes', []),
                    raw_unit.get('groups', []))

    for each in objects:
        router.register_route(each['uuid'], each['route'])


def gather_uuids_from_cache(cache: dict,
                            uuid_master: unite.UUIDMaster) -> None:
    """Find all UUIDs in given unit and store them into UUID master."""
    for fields in cache.get('variables', {}).values():
        for value in fields.values():
            uuid_master.add_existing_uuid(value)

    uuid_master.insert_queue(cache.get('uuids', []))


def gather_variables_from_cache(cache: dict,
                                identity_master: unite.IdentityMaster) -> None:
    """Find all variables in given cache and store them in Identity master."""
    for fields in cache.get('variables', {}).values():
        for variable, value in fields.items():
            identity_master.add_variable(variable, value)
