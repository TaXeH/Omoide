# -*- coding: utf-8 -*-

"""Implementation of a build operation.
"""
import sys

import omoide.use_cases.commands
from omoide import core
from omoide.core import extend
from omoide.database import constants as db_constants
from omoide.database import operations as db_operations
from omoide.use_cases import cli
from omoide.use_cases.freeze import database as db_build
from sqlalchemy.orm import sessionmaker
from omoide.database import models
from omoide.database import common


def build(command: omoide.use_cases.commands.FreezeCommand, filesystem: core.Filesystem,
          stdout: core.STDOut) -> None:
    """Create static database."""
    root_db_path = filesystem.join(command.sources_folder,
                                   db_constants.ROOT_DB_FILENAME)
    target_db_path = filesystem.join(command.content_folder,
                                     db_constants.STATIC_DB_FILENAME)

    if filesystem.not_exists(root_db_path):
        stdout.red(f'Source root database does not exist: {root_db_path}')
        sys.exit(1)

    if filesystem.exists(target_db_path):
        stdout.yellow(f'Deleting old target database: {target_db_path}')
        filesystem.delete_file(target_db_path)

    # database = db_operations.create_database(
    #     folder=command.sources_path,
    #     filename=db_constants.ROOT_DB_FILENAME,
    #     filesystem=filesystem,
    #     stdout=stdout,
    #     echo=True,
    # )



    # realms = session.query(models.Realm).all()
    # for each in realms:
    #     print(each)

    target_database = db_operations.create_database(
        folder=command.content_folder,
        filename=db_constants.STATIC_DB_FILENAME,
        filesystem=filesystem,
        stdout=stdout,
        echo=True,
    )
    # Session = sessionmaker(bind=target_database)
    # session = Session()
    # common.Base.metadata.create_all(bind=target_database)
    db_operations.create_scheme(target_database, stdout)

    # realms = db_build.get_all_realms(database)
    # themes = db_build.get_all_themes(database)
    # groups = db_build.get_all_groups(database)
    # metas = db_build.get_all_metas(database)
    # # users = db_build.get_all_users(database)
    #
    # for theme in themes.values():
    #     realm = realms[theme.realm_uuid]
    #     themes[theme.uuid] = extend.theme_from_realm(theme, realm)
    #
    # for group in groups.values():
    #     theme = themes[group.theme_uuid]
    #     groups[group.uuid] = extend.group_from_theme(group, theme)
    #
    # for meta in metas.values():
    #     realm = realms[meta.realm_uuid]
    #     group = groups.get(meta.group_uuid, core.Group())
    #     theme = themes[meta.theme_uuid]
    #     metas[meta.uuid] = extend.meta_from_all(meta, realm, theme, group)
    #     realm.statistics.add(meta.registered_on, meta.size, meta.tags)
    #     theme.statistics.add(meta.registered_on, meta.size, meta.tags)
    #     group.statistics.add(meta.registered_on, meta.size, meta.tags)


if __name__ == '__main__':
    cmd = omoide.use_cases.commands.FreezeCommand(
        sources_path='D:\\PycharmProjects\\Omoide\\example\\sources',
        content_path='D:\\PycharmProjects\\Omoide\\example\\content',
    )
    fs = core.Filesystem()
    st = core.STDOut()
    build(cmd, filesystem=fs, stdout=st)
