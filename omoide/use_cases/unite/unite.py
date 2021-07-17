# -*- coding: utf-8 -*-

"""Process source files.
"""
import json

from omoide import constants
from omoide import core
from omoide import use_cases
from omoide.use_cases import unite
from omoide.use_cases.unite import ephemeral
from omoide.use_cases.unite import identity
from omoide.use_cases.unite import preprocessing
from omoide.use_cases import transient


def act(command: use_cases.UniteCommand,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Process source files.
    """
    router = unite.Router()
    identity_master = unite.IdentityMaster()
    uuid_master = unite.UUIDMaster()
    renderer = use_cases.Renderer()

    identity.gather_existing_identities(
        storage_folder=command.storage_folder,
        router=router,
        identity_master=identity_master,
        uuid_master=uuid_master,
        filesystem=filesystem,
    )

    walk = use_cases.utils.walk_sources_from_command(command, filesystem)

    total_new_units = 0
    for branch, leaf, leaf_folder in walk:

        source_file_path = filesystem.join(leaf_folder,
                                           constants.SOURCE_FILE_NAME)

        if filesystem.not_exists(source_file_path):
            stdout.gray(f'\t[{branch}][{leaf}] Source file does not exist')
            continue

        make_unit_in_leaf(
            command=command,
            branch=branch,
            leaf=leaf,
            leaf_folder=leaf_folder,
            router=router,
            identity_master=identity_master,
            uuid_master=uuid_master,
            renderer=renderer,
            filesystem=filesystem,
            stdout=stdout,
        )
        stdout.green(f'\t[{branch}][{leaf}] Created unit file')
        total_new_units += 1

    return total_new_units


def make_unit_in_leaf(command: use_cases.UniteCommand, branch: str, leaf: str,
                      leaf_folder: str, router: unite.Router,
                      identity_master: unite.IdentityMaster,
                      uuid_master: unite.UUIDMaster,
                      renderer: use_cases.Renderer,
                      filesystem: core.Filesystem,
                      stdout: core.STDOut) -> str:
    """Create single unit file."""
    unit = make_unit(
        branch=branch,
        leaf=leaf,
        leaf_folder=leaf_folder,
        router=router,
        identity_master=identity_master,
        uuid_master=uuid_master,
        filesystem=filesystem,
        renderer=renderer
    )

    used_variables = identity_master.extract(branch, leaf)
    unit.variables.update(used_variables)

    used_uuids = uuid_master.extract_queue()
    uuid_master.clear_queue()

    unit_folder = filesystem.join(command.storage_folder, branch, leaf)
    unit_path = filesystem.join(unit_folder, constants.UNIT_FILE_NAME)
    uuids_path = filesystem.join(unit_folder, constants.UUIDS_FILE_NAME)

    filesystem.ensure_folder_exists(unit_folder, stdout)

    filesystem.write_json(unit_path, unit.dict())
    filesystem.write_json(uuids_path, used_uuids)

    return unit_path


def make_unit(branch: str, leaf: str, leaf_folder: str,
              router: unite.Router,
              identity_master: unite.IdentityMaster,
              uuid_master: unite.UUIDMaster,
              filesystem: core.Filesystem,
              renderer: use_cases.Renderer) -> transient.Unit:
    """Combine all updates in big JSON file."""
    source_path = filesystem.join(leaf_folder, constants.SOURCE_FILE_NAME)
    source_raw_text = filesystem.read_file(source_path)
    source_text = preprocessing.preprocess_source(source_raw_text, branch,
                                                  leaf)
    source_dict = json.loads(source_text)
    source = ephemeral.Source(**source_dict)
    unit = transient.Unit()

    preprocessing.do_realms(source, unit, router, identity_master, uuid_master)
    preprocessing.do_themes(source, unit, router,
                            identity_master, uuid_master)
    preprocessing.do_groups(source, unit, router, identity_master,
                            uuid_master, filesystem, leaf_folder,
                            renderer)
    preprocessing.do_no_group_metas(source, unit, router,
                                    identity_master,
                                    uuid_master, filesystem,
                                    leaf_folder, renderer)
    preprocessing.do_users(source, unit,
                           identity_master, uuid_master)

    return unit
