# -*- coding: utf-8 -*-

"""Process source files.
"""
import json
import sys
from typing import Optional, NoReturn

from omoide import commands
from omoide import constants
from omoide import infra
from omoide.migration_engine import classes
from omoide.migration_engine import raw_entities
from omoide.migration_engine import entities
from omoide.migration_engine.operations import unite


def act(command: commands.UniteCommand,
        filesystem: infra.Filesystem,
        stdout: infra.STDOut) -> int:
    """Process source files.
    """
    router = unite.Router()
    identity_master = unite.IdentityMaster()
    uuid_master = unite.UUIDMaster()
    renderer = classes.Renderer()

    unite.identity.gather_existing_identities(
        storage_folder=command.storage_folder,
        router=router,
        identity_master=identity_master,
        uuid_master=uuid_master,
        filesystem=filesystem,
    )

    walk = infra.walk_sources_from_command(command, filesystem)

    total_new_units = 0
    for branch, leaf, leaf_folder in walk:

        source_path = filesystem.join(leaf_folder, constants.SOURCE_FILE_NAME)
        if filesystem.not_exists(source_path):
            stdout.gray(f'\t[{branch}][{leaf}] Source file does not exist')
            continue

        unit_path = filesystem.join(command.storage_folder, branch, leaf,
                                    constants.UNIT_FILE_NAME)
        if filesystem.exists(unit_path) and not command.force:
            stdout.cyan(f'\t[{branch}][{leaf}] Unit file already exist')
            continue

        make_unit_in_leaf(command=command,
                          branch=branch,
                          leaf=leaf,
                          leaf_folder=leaf_folder,
                          router=router,
                          identity_master=identity_master,
                          uuid_master=uuid_master,
                          renderer=renderer,
                          filesystem=filesystem,
                          stdout=stdout)

        stdout.green(f'\t[{branch}][{leaf}] Created unit file')
        total_new_units += 1

    return total_new_units


# pylint: disable=too-many-locals
def make_unit_in_leaf(command: commands.UniteCommand, branch: str, leaf: str,
                      leaf_folder: str, router: unite.Router,
                      identity_master: unite.IdentityMaster,
                      uuid_master: unite.UUIDMaster,
                      renderer: classes.Renderer,
                      filesystem: infra.Filesystem,
                      stdout: infra.STDOut) -> str:
    """Create single unit file."""
    unit = make_unit(branch=branch,
                     leaf=leaf,
                     leaf_folder=leaf_folder,
                     router=router,
                     identity_master=identity_master,
                     uuid_master=uuid_master,
                     filesystem=filesystem,
                     renderer=renderer)

    cache = {
        'variables': identity_master.extract(branch, leaf),
        'uuids': uuid_master.extract_queue(),
    }
    uuid_master.clear_queue()

    unit_folder = filesystem.join(command.storage_folder, branch, leaf)
    filesystem.ensure_folder_exists(unit_folder, stdout)

    unit_path = filesystem.join(unit_folder, constants.UNIT_FILE_NAME)
    unit_dict = unit.dict()
    unit_text = json.dumps(unit_dict)
    assert_no_variables(unit_text, stdout)
    filesystem.write_json(unit_path, unit_dict)

    cache_path = filesystem.join(unit_folder, constants.CACHE_FILE_NAME)
    filesystem.write_json(cache_path, cache)

    return unit_path


def make_unit(branch: str,
              leaf: str,
              leaf_folder: str,
              router: unite.Router,
              identity_master: unite.IdentityMaster,
              uuid_master: unite.UUIDMaster,
              filesystem: infra.Filesystem,
              renderer: classes.Renderer) -> entities.Unit:
    """Combine all updates in big JSON file."""
    source_path = filesystem.join(leaf_folder, constants.SOURCE_FILE_NAME)
    source_raw_text = filesystem.read_file(source_path)
    source_text = unite.preprocessing.preprocess_source(
        text=source_raw_text,
        branch=branch,
        leaf=leaf,
        identity_master=identity_master,
        uuid_master=uuid_master,
    )
    source_dict = json.loads(source_text)
    source = raw_entities.Source(**source_dict)

    unit = entities.Unit()
    unite.preprocessing.do_themes(source, unit, router)
    unite.preprocessing.do_groups(source, unit, router,
                                  uuid_master, filesystem,
                                  leaf_folder, renderer)
    unite.preprocessing.do_synonyms(source, unit)
    unite.preprocessing.do_no_group_metas(source, unit, router, uuid_master,
                                          filesystem, leaf_folder, renderer)

    return unit


def assert_no_variables(unit_text: str,
                        stdout: infra.STDOut) -> Optional[NoReturn]:
    """Raise if variables are still present in output."""
    index = unit_text.find(constants.VARIABLE_SIGN)
    if index != -1:
        left = max(index - constants.VARIABLE_SEARCH_WINDOW, 0)
        right = index + constants.VARIABLE_SEARCH_WINDOW
        fragment = unit_text[left:right]
        stdout.red(
            'Seems like output unit still contains some variables:'
            f'\n...{fragment}...\n'
        )
        sys.exit(1)
