# -*- coding: utf-8 -*-

"""Prepare resources and launch application.
"""
from omoide.manage import main as manage
from omoide.migration_engine import persistent


def main():
    """Entry point.
    """
    # added to avoid constant updates in example with each release
    # not really supposed to be used in actual work
    persistent.set_now('2021-07-17 00:00:00')
    persistent.set_today('2021-07-17')
    persistent.set_revision('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    # manage(['unite', '--force'])
    # manage(['make_migrations', '--force'])
    # manage(['make_relocations', '--force'])
    # manage(['migrate', '--force'])
    # manage(['relocate', '--force'])
    # manage(['sync', '--force'])
    # manage(['freeze'])
    manage(['runserver'])


if __name__ == '__main__':
    main()
