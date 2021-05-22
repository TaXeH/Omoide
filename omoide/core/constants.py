# -*- coding: utf-8 -*-

"""Constant values for the search engine.
"""
import re
from enum import Enum, unique
from typing import Set


# pylint: disable=R0903
class TokensMixin:
    """Simplifies extraction of values from enum."""
    __members__ = {}

    @classmethod
    def tokens(cls) -> Set[str]:
        """Return values of all class fields."""
        return {x.value for x in cls.__members__.values()}


@unique
class ImageResolutionMpx(TokensMixin, Enum):
    """Enumerations of standard image resolutions.
    """
    RESOLUTION_TINY = 'TINY'
    RESOLUTION_SMALL = 'SMALL'
    RESOLUTION_MEAN = 'MEAN'
    RESOLUTION_BIG = 'BIG'
    RESOLUTION_HUGE = 'HUGE'


@unique
class ImageResolutionThreshold(Enum):
    """Enumerations of standard image resolution thresholds (megapixels).
    """
    THRESHOLD_TINY = 0.1
    THRESHOLD_SMALL = 1.0
    THRESHOLD_MEAN = 5.0
    THRESHOLD_BIG = 10.0


@unique
class MediaDuration(TokensMixin, Enum):
    """Enumerations of standard video/audio durations.
    """
    DURATION_MOMENT = 'MOMENT'
    DURATION_SHORT = 'SHORT'
    DURATION_MEDIUM = 'MEDIUM'
    DURATION_LONG = 'LONG'


@unique
class DurationThreshold(Enum):
    """Enumerations of standard video/audio thresholds (seconds).
    """
    THRESHOLD_MOMENT = 5
    THRESHOLD_SHORT = 300
    THRESHOLD_MEDIUM = 2400


@unique
class MediaType(TokensMixin, Enum):
    """Enumerations of standard media types.
    """
    TYPE_IMAGE = 'IMAGE'
    TYPE_GIF = 'GIF'
    TYPE_VIDEO = 'VIDEO'
    TYPE_AUDIO = 'AUDIO'


@unique
class Flags(TokensMixin, Enum):
    """Enumerations of standard search flags.
    """
    FLAG_DESC = 'desc'
    FLAG_DEMAND = 'demand'


@unique
class Operators(TokensMixin, Enum):
    """Enumerations of standard search keywords.
    """
    KW_AND = '+'
    KW_OR = '|'
    KW_NOT = '-'
    KW_FLAG = '~'
    KW_INCLUDE_R = '&&'
    KW_EXCLUDE_R = '!!'
    KW_INCLUDE_T = '&'
    KW_EXCLUDE_T = '!'


KEYWORDS = frozenset([
    *ImageResolutionMpx.tokens(),
    *MediaType.tokens(),
    *MediaDuration.tokens(),
    *Flags.tokens(),
    *Operators.tokens(),
])

CASE_SENSITIVE = frozenset([
    *ImageResolutionMpx.tokens(),
    *MediaType.tokens(),
    *MediaDuration.tokens(),
])

PREFIX_REALM = 'r'
PREFIX_THEME = 't'
PREFIX_GROUP = 'g'
PREFIX_META = 'm'
PREFIX_SYNONYM = 's'
PREFIX_IMPL_TAG = 'i'
PREFIX_USER = 'u'
ALL_PREFIXES = ''.join([PREFIX_REALM,
                        PREFIX_THEME,
                        PREFIX_GROUP,
                        PREFIX_META,
                        PREFIX_SYNONYM,
                        PREFIX_IMPL_TAG,
                        PREFIX_USER])

ALL_REALMS = 'all_realms'
ALL_THEMES = 'all_themes'
NEVER_FIND_THIS = 'ʕ•ᴥ•ʔ'
UNKNOWN = 'UNKNOWN'
UUID_PATTERN = re.compile(r'\$[' + ALL_PREFIXES + r']_\d+')
COMMON_GROUP = 'other'
VARIABLE_SIGN = '$'
