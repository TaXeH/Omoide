# -*- coding: utf-8 -*-

"""Prepare resources and launch application.
"""
from omoide.manage import main as manage


def main():
    """Entry point.
    """
    manage(['make_migrations'])
    # manage(['migrate'])
    # manage(['sync'])
    # manage(['runserver'])


if __name__ == '__main__':
    main()
