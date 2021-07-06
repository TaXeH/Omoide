# -*- coding: utf-8 -*-

"""Tools required to generate unique identifiers.
"""
import random
import string
from datetime import datetime
from functools import lru_cache
from itertools import chain

from omoide import constants
from omoide import core


@lru_cache()
def get_today() -> str:
    """Get today date as a string."""
    return str(datetime.now().date())


@lru_cache()
def get_now() -> str:
    """Get current moment as a string.

    Note that we're using only one moment
    for all operations through all migration creation.
    """
    return str(datetime.now().replace(microsecond=0))


@lru_cache()
def get_revision_number(length: int = constants.REVISION_LEN) -> str:
    """Generate unique revision number from os random generator."""
    symbols = string.ascii_lowercase + string.digits
    tokens = [random.choice(symbols) for _ in range(length)]
    return ''.join(tokens)


def gather_existing_identities(sources_folder: str,
                               router: core.Router,
                               identity_master: core.IdentityMaster,
                               uuid_master: core.UUIDMaster,
                               filesystem: core.Filesystem) -> None:
    """Get all variables and all UUID from existing files."""
    for trunk in filesystem.list_folders(sources_folder):
        trunk_folder = filesystem.join(sources_folder, trunk)
        for leaf in filesystem.list_folders(trunk_folder):
            leaf_folder = filesystem.join(trunk_folder, leaf)
            update_file_path = filesystem.join(leaf_folder,
                                               constants.UNIT_FILENAME)

            if filesystem.not_exists(update_file_path):
                continue

            content = filesystem.read_json(update_file_path)
            gather_routes_from_processed_source(content, router)
            gather_uuids_from_processed_source(content, uuid_master)
            gather_variables_from_processed_source(content, identity_master)


def gather_routes_from_processed_source(content: dict,
                                        router: core.Router
                                        ) -> None:
    """Find all routes in given file and store them into router."""
    objects = chain(
        content.get('realms', []),
        content.get('themes', []),
        content.get('groups', []),
    )

    for each in objects:
        router.register_route(each['uuid'], each['route'])


def gather_uuids_from_processed_source(content: dict,
                                       uuid_master: core.UUIDMaster
                                       ) -> None:
    """Find all UUIDs in given file and store them into UUID master."""
    # print('gather_uuids_from_processed_source', content)
    # FIXME


def gather_variables_from_processed_source(content: dict,
                                           identity_master: core.IdentityMaster
                                           ) -> None:
    """Find all variables in given file and store them into Identity master."""
    # print('gather_variables_from_processed_source', content)
    # FIXME
