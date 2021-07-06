# -*- coding: utf-8 -*-

"""Process source files.
"""
import json
from typing import Any, Dict

from omoide import constants
from omoide import core
from omoide.files.operations import drop_files
from omoide.use_cases import commands, identity
from omoide.use_cases.unite import preprocessing


def act(command: commands.UniteCommand, filesystem: core.Filesystem,
        stdout: core.STDOut) -> int:
    """Process source files.
    """
    filenames_to_delete = {
        constants.UNIT_FILENAME,
        constants.MIGRATION_FILENAME,
    }
    drop_files(command, filenames_to_delete, filesystem, stdout)

    router = core.Router()
    identity_master = core.IdentityMaster()
    uuid_master = core.UUIDMaster()
    renderer = core.Renderer()

    identity.gather_existing_identities(command.sources_folder,
                                        router,
                                        identity_master,
                                        uuid_master,
                                        filesystem)

    total_new_migrations = 0
    for trunk in filesystem.list_folders(command.sources_folder):

        if command.trunk != 'all' and command.trunk != trunk:
            continue

        trunk_folder = filesystem.join(command.sources_folder, trunk)
        for leaf in filesystem.list_folders(trunk_folder):

            if command.leaf != 'all' and command.leaf != leaf:
                continue

            leaf_folder = filesystem.join(trunk_folder, leaf)
            unite_single_leaf(
                source_folder=command.sources_folder,
                content_folder=command.content_folder,
                trunk=trunk,
                leaf=leaf,
                leaf_folder=leaf_folder,
                router=router,
                identity_master=identity_master,
                uuid_master=uuid_master,
                renderer=renderer,
                filesystem=filesystem,
                stdout=stdout,
            )
            total_new_migrations += 1

    return total_new_migrations


def unite_single_leaf(
        source_folder: str, content_folder: str,
        trunk: str, leaf: str, leaf_folder: str,
        router: core.Router,
        identity_master: core.IdentityMaster,
        uuid_master: core.UUIDMaster,
        renderer: core.Renderer,
        filesystem: core.Filesystem,
        stdout: core.STDOut) -> None:
    """Create all migration resources for a single folder."""
    stdout.print(f'Uniting {leaf_folder}')

    source_file_path = filesystem.join(leaf_folder,
                                       constants.SOURCE_FILENAME)

    if filesystem.not_exists(source_file_path):
        stdout.yellow(f'Source file does not exist: {source_file_path}')
        return

    update_file = make_update_file(
        trunk,
        leaf,
        leaf_folder,
        router,
        identity_master,
        uuid_master,
        filesystem,
        renderer
    )

    update_file_path = filesystem.join(leaf_folder,
                                       constants.UNIT_FILENAME)

    filesystem.write_json(update_file_path, update_file)
    stdout.yellow(f'Created update file: {update_file_path}')


def make_update_file(trunk: str, leaf: str, leaf_folder: str,
                     router: core.Router,
                     identity_master: core.IdentityMaster,
                     uuid_master: core.UUIDMaster,
                     filesystem: core.Filesystem,
                     renderer: core.Renderer) -> Dict[str, Any]:
    """Combine all updates in big JSON file."""
    source_file_path = filesystem.join(leaf_folder,
                                       constants.SOURCE_FILENAME)
    source_raw_text = filesystem.read_file(source_file_path)
    source_text = preprocessing.preprocess_source(source_raw_text, trunk, leaf)
    source = json.loads(source_text)

    update = {
        'variables': {},

        'realms': [],
        'themes': [],
        'groups': [],
        'metas': [],
        'users': [],

        'permissions_realm': [],
        'permissions_themes': [],
        'permissions_groups': [],
        'permissions_metas': [],
        'permissions_users': [],

        'tags_realms': [],
        'tags_themes': [],
        'tags_groups': [],
        'tags_metas': [],

        'synonyms': [],
        'implicit_tags': [],
    }
    preprocessing.preprocess_realms(source, update, router,
                                    identity_master, uuid_master)
    preprocessing.preprocess_themes(source, update, router,
                                    identity_master, uuid_master)
    preprocessing.preprocess_groups(source, update, router, identity_master,
                                    uuid_master, filesystem, leaf_folder,
                                    renderer)
    preprocessing.preprocess_no_group_metas(source, update, router,
                                            identity_master,
                                            uuid_master, filesystem,
                                            leaf_folder, renderer)
    preprocessing.preprocess_users(source, update,
                                   identity_master, uuid_master)

    used_variables = identity_master.to_dict()
    update['variables'].update(used_variables)
    identity_master.freeze()

    return update


if __name__ == '__main__':
    _command = commands.UniteCommand(
        trunk='all',
        leaf='all',
        sources_folder='D:\\PycharmProjects\\Omoide\\example\\sources',
        content_folder='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    _filesystem = core.Filesystem()
    _stdout = core.STDOut()
    act(_command, _filesystem, _stdout)
