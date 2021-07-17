# -*- coding: utf-8 -*-

"""Prepare resources and launch application.
"""
from omoide.manage import main as manage
from omoide.use_cases.unite import persistent


def main():
    """Entry point.
    """
    # added to avoid constant updates in example with each release
    # not really supposed to be used in actual work
    persistent.set_now('2021-07-17 00:00:00')
    persistent.set_today('2021-07-17')
    persistent.set_revision('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    # manage(['unite', 'all', 'all'])
    # manage(['make_migrations', 'all', 'all'])
    # manage(['make_relocations', 'all', 'all'])
    # manage(['migrate', 'all', 'all'])
    # manage(['relocate', 'all', 'all'])
    manage(['sync', 'all', 'all'])
    # manage(['freeze'])
    # manage(['runserver'])


if __name__ == '__main__':
    main()
