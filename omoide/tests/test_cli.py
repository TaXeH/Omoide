# -*- coding: utf-8 -*-

"""Tests.
"""
from functools import partial

import pytest

from omoide.use_cases import commands
from omoide.use_cases import cli
from omoide.use_cases import constants

parse = partial(cli.parse_arguments, sources_path=None, content_path=None)


def test_makemigration_all():
    op1 = parse(['unite'])
    op2 = parse(['unite', 'all'])
    op3 = parse(['unite', 'all', 'all'])

    assert op1 == op2 == op3

    assert isinstance(op1, commands.MakeMigrationsCommand)
    assert op1.trunk == 'all'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_makemigration_trunk():
    op1 = parse(['unite', 'folder'])
    op2 = parse(['unite', 'folder', 'all'])

    assert op1 == op2

    assert isinstance(op1, commands.MakeMigrationsCommand)
    assert op1.trunk == 'folder'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_makemigration_leaf():
    op = parse(['unite', 'folder', 'some'])

    assert isinstance(op, commands.MakeMigrationsCommand)
    assert op.trunk == 'folder'
    assert op.leaf == 'some'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_makemigration_paths():
    op = cli.parse_arguments(['unite',
                              '--sources', 'test1',
                              '--content', 'test2'], None, None)

    assert isinstance(op, commands.MakeMigrationsCommand)
    assert op.trunk == 'all'
    assert op.leaf == 'all'
    assert op.sources_folder == 'test1'
    assert op.content_folder == 'test2'


def test_migrate_all():
    op1 = parse(['migrate'])
    op2 = parse(['migrate', 'all'])
    op3 = parse(['migrate', 'all', 'all'])

    assert op1 == op2 == op3

    assert isinstance(op1, commands.MigrateCommand)
    assert op1.trunk == 'all'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_migrate_trunk():
    op1 = parse(['migrate', 'folder'])
    op2 = parse(['migrate', 'folder', 'all'])

    assert op1 == op2

    assert isinstance(op1, commands.MigrateCommand)
    assert op1.trunk == 'folder'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_migrate_leaf():
    op = parse(['migrate', 'folder', 'some'])

    assert isinstance(op, commands.MigrateCommand)
    assert op.trunk == 'folder'
    assert op.leaf == 'some'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_migrate_all_leaves():
    msg = r'You cannot use all trunks with specific leaf \(given folder\)'
    with pytest.raises(ValueError, match=msg):
        parse(['migrate', 'all', 'folder'])


def test_migrate_paths():
    op = cli.parse_arguments(['migrate',
                              '--sources', 'test1',
                              '--content', 'test2'], None, None)

    assert isinstance(op, commands.MigrateCommand)
    assert op.trunk == 'all'
    assert op.leaf == 'all'
    assert op.sources_folder == 'test1'
    assert op.content_folder == 'test2'


def test_migrate_not_enough_paths():
    msg = r'You need to specify value for --content parameter'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['migrate', '--sources', 'test1',
                             '--content'], None, None)


def test_sync_all():
    op = cli.parse_arguments(['sync'], None, None)

    assert isinstance(op, commands.SyncCommand)
    assert op.trunk == 'all'
    assert op.leaf == 'all'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_sync_trunk():
    op = cli.parse_arguments(['sync', 'trunk', 'test1'], None, None)

    assert isinstance(op, commands.SyncCommand)
    assert op.trunk == 'test1'
    assert op.leaf == 'all'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_sync_leaf():
    op = cli.parse_arguments(['sync', 'leaf', 'test2'], None, None)

    assert isinstance(op, commands.SyncCommand)
    assert op.trunk == 'find'
    assert op.leaf == 'test2'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_sync_bad_target():
    msg = 'Unknown sync target wtf'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['sync', 'wtf', 'test2'], None, None)


def test_sync_not_enough_parameters():
    msg = r'To perform sync you need to ' \
          r'supply target \(trunk or leaf\) and a folder name'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['sync', 'wtf'], None, None)


def test_runserver_bare():
    op = cli.parse_arguments(['runserver'], None, None)

    assert isinstance(op, commands.RunserverCommand)
    assert op.host == constants.DEFAULT_SERVER_HOST
    assert op.port == constants.DEFAULT_SERVER_PORT
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_runserver_port():
    op = cli.parse_arguments(['runserver', '8888'], None, None)

    assert isinstance(op, commands.RunserverCommand)
    assert op.host == constants.DEFAULT_SERVER_HOST
    assert op.port == 8888
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_runserver_full():
    op = cli.parse_arguments(['runserver', '192.168.1.67:8888'], None, None)

    assert isinstance(op, commands.RunserverCommand)
    assert op.host == '192.168.1.67'
    assert op.port == 8888
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_runserver_wrong_port():
    msg = 'Wrong port for server xxx'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['runserver', '192.168.1.67:xxx'], None, None)


def test_bad_command():
    msg = 'Unknown command: wtf'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['wtf'], None, None)
