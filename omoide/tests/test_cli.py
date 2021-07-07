# -*- coding: utf-8 -*-

"""Tests.
"""
from functools import partial

import pytest

from omoide import constants
from omoide.use_cases import cli
from omoide.use_cases import commands

parse = partial(cli.parse_arguments, sources_folder=None, content_folder=None)


def test_make_migrations_all():
    _, op1 = parse(['make_migrations'])
    _, op2 = parse(['make_migrations', 'all'])
    _, op3 = parse(['make_migrations', 'all', 'all'])

    assert op1 == op2 == op3

    assert isinstance(op1, commands.MakeMigrationsCommand)
    assert op1.branch == 'all'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_make_migrations_branch():
    _, op1 = parse(['make_migrations', 'folder'])
    _, op2 = parse(['make_migrations', 'folder', 'all'])

    assert op1 == op2

    assert isinstance(op1, commands.MakeMigrationsCommand)
    assert op1.branch == 'folder'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_make_migrations_leaf():
    cmd, op = parse(['make_migrations', 'folder', 'some'])

    assert cmd == 'make_migrations'
    assert isinstance(op, commands.MakeMigrationsCommand)
    assert op.branch == 'folder'
    assert op.leaf == 'some'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_make_migration_paths():
    cmd, op = cli.parse_arguments(['make_migrations',
                                   '--sources', 'test1',
                                   '--content', 'test2'], None, None)

    assert cmd == 'make_migrations'
    assert isinstance(op, commands.MakeMigrationsCommand)
    assert op.branch == 'all'
    assert op.leaf == 'all'
    assert op.sources_folder == 'test1'
    assert op.content_folder == 'test2'


def test_migrate_all():
    _, op1 = parse(['migrate'])
    _, op2 = parse(['migrate', 'all'])
    _, op3 = parse(['migrate', 'all', 'all'])

    assert op1 == op2 == op3

    assert isinstance(op1, commands.MigrateCommand)
    assert op1.branch == 'all'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_migrate_branch():
    _, op1 = parse(['migrate', 'folder'])
    _, op2 = parse(['migrate', 'folder', 'all'])

    assert op1 == op2

    assert isinstance(op1, commands.MigrateCommand)
    assert op1.branch == 'folder'
    assert op1.leaf == 'all'
    assert op1.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op1.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_migrate_leaf():
    _, op = parse(['migrate', 'folder', 'some'])

    assert isinstance(op, commands.MigrateCommand)
    assert op.branch == 'folder'
    assert op.leaf == 'some'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_migrate_all_leaves():
    msg = r'You cannot use all branchs with specific leaf \(given folder\)'
    with pytest.raises(ValueError, match=msg):
        parse(['migrate', 'all', 'folder'])


def test_migrate_paths():
    cmd, op = cli.parse_arguments(['migrate',
                                   '--sources', 'test1',
                                   '--content', 'test2'], None, None)

    assert cmd == 'migrate'
    assert isinstance(op, commands.MigrateCommand)
    assert op.branch == 'all'
    assert op.leaf == 'all'
    assert op.sources_folder == 'test1'
    assert op.content_folder == 'test2'


def test_migrate_not_enough_paths():
    msg = r'You need to specify value for --content parameter'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['migrate', '--sources', 'test1',
                             '--content'], None, None)


def test_sync_all():
    cmd, op = cli.parse_arguments(['sync'], None, None)

    assert cmd == 'sync'
    assert isinstance(op, commands.SyncCommand)
    assert op.branch == 'all'
    assert op.leaf == 'all'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_sync_branch():
    cmd, op = cli.parse_arguments(['sync', 'branch', 'test1'], None, None)

    assert cmd == 'sync'
    assert isinstance(op, commands.SyncCommand)
    assert op.branch == 'test1'
    assert op.leaf == 'all'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_sync_leaf():
    cmd, op = cli.parse_arguments(['sync', 'leaf', 'test2'], None, None)

    assert cmd == 'sync'
    assert isinstance(op, commands.SyncCommand)
    assert op.branch == 'find'
    assert op.leaf == 'test2'
    assert op.sources_folder == constants.DEFAULT_SOURCES_FOLDER
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_sync_bad_target():
    msg = 'Unknown sync target wtf'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['sync', 'wtf', 'test2'], None, None)


def test_sync_not_enough_parameters():
    msg = r'To perform sync you need to ' \
          r'supply target \(branch or leaf\) and a folder name'
    with pytest.raises(ValueError, match=msg):
        cli.parse_arguments(['sync', 'wtf'], None, None)


def test_runserver_bare():
    cmd, op = cli.parse_arguments(['runserver'], None, None)

    assert cmd == 'runserver'
    assert isinstance(op, commands.RunserverCommand)
    assert op.host == constants.DEFAULT_SERVER_HOST
    assert op.port == constants.DEFAULT_SERVER_PORT
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_runserver_port():
    cmd, op = cli.parse_arguments(['runserver', '8888'], None, None)

    assert cmd == 'runserver'
    assert isinstance(op, commands.RunserverCommand)
    assert op.host == constants.DEFAULT_SERVER_HOST
    assert op.port == 8888
    assert op.content_folder == constants.DEFAULT_CONTENT_FOLDER


def test_runserver_full():
    cmd, op = cli.parse_arguments(['runserver', '192.168.1.67:8888'],
                                  None, None)

    assert cmd == 'runserver'
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
