# -*- coding: utf-8 -*-

"""Prepare resources and launch application.
"""
from omoide.__main__ import cli as manage
from omoide.migration_engine.operations.unite import persistent


def main():
    """Entry point.
    """
    # added to avoid constant updates in example with each release
    # not really supposed to be used in actual work
    persistent.set_now('2021-08-20 00:00:00')
    persistent.set_revision('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    manage(['unite'])
    # manage(['make_migrations'])
    # manage(['make_relocations'])
    # manage(['migrate'])
    # manage(['relocate'])
    # manage(['sync'])
    # manage(['freeze'])
    # manage(['runserver'])


if __name__ == '__main__':
    main()
