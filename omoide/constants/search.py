# -*- coding: utf-8 -*-

"""Constant values.
"""
# search engine
NEVER_FIND_THIS = 'ʕ•ᴥ•ʔ'
UNKNOWN = 'UNKNOWN'
ALL_REALMS = 'all_realms'
ALL_THEMES = 'all_themes'
ALL_GROUPS = 'all_groups'
NO_GROUP = 'no_group'

# identity
PREFIX_REALM = 'r'
PREFIX_THEME = 't'
PREFIX_SYNONYM = 's'
PREFIX_IMPLICIT_TAG = 'i'
PREFIX_GROUP = 'g'
PREFIX_META = 'm'
PREFIX_USER = 'u'

ALL_PREFIXES = ''.join([
    PREFIX_REALM,
    PREFIX_THEME,
    PREFIX_SYNONYM,
    PREFIX_IMPLICIT_TAG,
    PREFIX_GROUP,
    PREFIX_META,
    PREFIX_USER,
])
ALL_PREFIXES_SET = set(ALL_PREFIXES)

VARIABLE_SIGN = '$'
UUID_VARIABLE_PATTERN = r'\$[' + ALL_PREFIXES + r']_\d+'
UUID_LONG_VARIABLE_PATTERN = r'\$.+\..+\.[' + ALL_PREFIXES + r']_\d+'

# search keywords
RESOLUTION_TINY = 'TINY'
RESOLUTION_SMALL = 'SMALL'
RESOLUTION_MEAN = 'MEAN'
RESOLUTION_BIG = 'BIG'
RESOLUTION_HUGE = 'HUGE'

ALL_RESOLUTIONS = {
    RESOLUTION_TINY,
    RESOLUTION_SMALL,
    RESOLUTION_MEAN,
    RESOLUTION_BIG,
    RESOLUTION_HUGE,
}

DURATION_MOMENT = 'MOMENT'
DURATION_SHORT = 'SHORT'
DURATION_MEDIUM = 'MEDIUM'
DURATION_LONG = 'LONG'

ALL_DURATIONS = {
    DURATION_MOMENT,
    DURATION_SHORT,
    DURATION_MEDIUM,
    DURATION_LONG,
}

THRESHOLD_RESOLUTION_TINY = 0.1
THRESHOLD_RESOLUTION_SMALL = 1.0
THRESHOLD_RESOLUTION_MEAN = 5.0
THRESHOLD_RESOLUTION_BIG = 10.0

ALL_RESOLUTION_THRESHOLDS = {
    THRESHOLD_RESOLUTION_TINY,
    THRESHOLD_RESOLUTION_SMALL,
    THRESHOLD_RESOLUTION_MEAN,
    THRESHOLD_RESOLUTION_BIG,
}

THRESHOLD_DURATION_MOMENT = 5
THRESHOLD_DURATION_SHORT = 300
THRESHOLD_DURATION_MEDIUM = 2400

ALL_DURATION_THRESHOLDS = {
    THRESHOLD_DURATION_MOMENT,
    THRESHOLD_DURATION_SHORT,
    THRESHOLD_DURATION_MEDIUM,
}

MEDIA_TYPE_IMAGE = 'IMAGE'
MEDIA_TYPE_GIF = 'GIF'
MEDIA_TYPE_VIDEO = 'VIDEO'
MEDIA_TYPE_AUDIO = 'AUDIO'

ALL_MEDIA_TYPES = {
    MEDIA_TYPE_IMAGE,
    MEDIA_TYPE_GIF,
    MEDIA_TYPE_VIDEO,
    MEDIA_TYPE_AUDIO,
}

FLAG_ASC = 'asc'
FLAG_DESC = 'desc'
FLAG_RAND = 'rand'

ALL_FLAGS = {
    FLAG_ASC,
    FLAG_DESC,
    FLAG_RAND,
}

KW_AND = '+'
KW_OR = '|'
KW_NOT = '-'
KW_FLAG = '~'

OPERATORS = {
    KW_AND,
    KW_OR,
    KW_NOT,
    KW_FLAG,
}

KEYWORDS = frozenset([
    *ALL_RESOLUTIONS,
    *ALL_DURATIONS,
    *ALL_MEDIA_TYPES,
    *ALL_FLAGS,
    *OPERATORS,
])

CASE_SENSITIVE = frozenset([
    *ALL_RESOLUTIONS,
    *ALL_DURATIONS,
    *ALL_MEDIA_TYPES,
])
