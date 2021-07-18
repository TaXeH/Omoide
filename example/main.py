# -*- coding: utf-8 -*-

"""Prepare resources and launch application.
"""
from omoide.manage import main as manage
from omoide.incarnation.unite import persistent


def main():
    """Entry point.
    """
    # added to avoid constant updates in example with each release
    # not really supposed to be used in actual work
    persistent.set_now('2021-07-17 00:00:00')
    persistent.set_today('2021-07-17')
    persistent.set_revision('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    manage(['unite'])
    manage(['make_migrations'])
    manage(['make_relocations'])
    manage(['migrate'])
    manage(['relocate'])
    manage(['sync'])
    manage(['freeze'])
    manage(['runserver'])


if __name__ == '__main__':
    main()
