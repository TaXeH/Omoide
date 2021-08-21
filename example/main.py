# -*- coding: utf-8 -*-

"""Prepare resources and launch application.
"""
from contextlib import suppress

from omoide.__main__ import cli as omoide_
from omoide.migration_engine.operations.unite import persistent


def main():
    """Entry point.
    """
    # added to avoid constant updates in example with each release
    # not really supposed to be used in actual work
    persistent.set_now('2021-08-20 00:00:00')
    persistent.set_revision('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    with suppress(SystemExit):
        omoide_(['unite'])

    # with suppress(SystemExit):
    #     omoide_(['make_migrations'])

    # with suppress(SystemExit):
    #     omoide_(['make_relocations'])

    # omoide_(['migrate'])
    # omoide_(['relocate'])
    # omoide_(['sync'])
    # omoide_(['freeze'])
    # omoide_(['runserver'])


if __name__ == '__main__':
    main()
