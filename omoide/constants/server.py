# -*- coding: utf-8 -*-

"""Constant values.
"""
import os as _os

VERSION = '2021-08-11'

DEFAULT_SERVER_HOST = '0.0.0.0'
DEFAULT_SERVER_PORT = 8000

# files and folders
TEMPLATES_FOLDER_NAME = 'templates'
STATIC_FOLDER_NAME = 'static'

DEFAULT_TEMPLATES_FOLDER = _os.path.join('.', TEMPLATES_FOLDER_NAME)
DEFAULT_STATIC_FOLDER = _os.path.join('.', STATIC_FOLDER_NAME)
