# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from omoide import constants
from omoide.vision.search.class_query import Query
from omoide.vision.search.class_query_builder import QueryBuilder


@pytest.fixture
def query_builder():
    inst = QueryBuilder(Query)
    return inst


@pytest.fixture
def empty_query_dict():
    return {
        'and_': [],
        'or_': [],
        'not_': [],
        'include_realms': [],
        'exclude_realms': [],
        'include_themes': [],
        'exclude_themes': [],
        'flags': [],
    }


@pytest.fixture
def bad_query_dict():
    return {
        'and_': [constants.NEVER_FIND_THIS],
        'or_': ['cats'],
        'not_': [],
        'include_realms': [],
        'exclude_realms': [],
        'include_themes': [],
        'exclude_themes': [],
        'flags': [],
    }


def test_query_builder_split_query(query_builder):
    f = query_builder.split_request_into_parts
    assert f('cats | dogs') == ['|', 'cats', '|', 'dogs']
    assert f('a + b - c') == ['|', 'a', '+', 'b', '-', 'c']
    assert f('x & y ~ f') == ['|', 'x', '&', 'y', '~', 'f']
    assert f('k ! d') == ['|', 'k', '!', 'd']


def test_query_builder_1(query_builder):
    text = 'cats | dogs'
    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': [],
        'exclude_realms': [],
        'exclude_themes': [],
        'flags': [],
        'include_realms': [],
        'include_themes': [],
        'not_': [],
        'or_': ['cats', 'dogs'],
    }
    assert str(query) == '| cats | dogs'


def test_query_builder_2(query_builder):
    text = '+ cats | dogs + turtle - frog + IMAGE & test'

    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': [constants.MEDIA_TYPE_IMAGE, 'cats', 'turtle'],
        'or_': ['dogs'],
        'not_': ['frog'],
        'exclude_realms': [],
        'exclude_themes': [],
        'flags': [],
        'include_realms': [],
        'include_themes': ['test'],
    }
    assert str(query) == '+ IMAGE + cats + turtle | dogs - frog & test'


def test_query_builder_3(query_builder):
    text = '|fly +fish !spiders +HUGE +AUDIO'
    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': [constants.MEDIA_TYPE_AUDIO,
                 constants.RESOLUTION_HUGE,
                 'fish'],
        'or_': ['fly'],
        'not_': [],
        'exclude_realms': [],
        'exclude_themes': ['spiders'],
        'flags': [],
        'include_realms': [],
        'include_themes': [],
    }
    assert str(query) == '+ AUDIO + HUGE + fish | fly ! spiders'


def test_query_builder_wrong_1(query_builder, bad_query_dict):
    text = 'cats + - dogs'
    query = query_builder.from_query(text)
    assert query.as_dict() == bad_query_dict
    assert str(query) == '+ ' + constants.NEVER_FIND_THIS + ' | cats'


def test_query_builder_empty(query_builder, empty_query_dict):
    text = ''
    query = query_builder.from_query(text)
    assert query.as_dict() == empty_query_dict
    assert str(query) == ''


def test_query_builder_flags(query_builder, empty_query_dict):
    text = '+some+other~demand~desc'
    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': ['other', 'some'],
        'or_': [],
        'not_': [],
        'include_realms': [],
        'include_themes': [],
        'flags': [constants.FLAG_DEMAND,
                  constants.FLAG_DESC],
        'exclude_realms': [],
        'exclude_themes': [],
    }
    assert str(query) == '+ other + some ~ demand ~ desc'


def test_query_builder_realm(query_builder):
    query = query_builder.from_query('', 'some_realm')
    assert query.as_dict() == {
        'and_': [],
        'or_': [],
        'not_': [],
        'include_realms': ['some_realm'],
        'include_themes': [],
        'flags': [],
        'exclude_realms': [],
        'exclude_themes': [],
    }
    assert str(query) == '&& some_realm'


def test_query_builder_theme(query_builder):
    query = query_builder.from_query('', '', 'some_theme')
    assert query.as_dict() == {
        'and_': [],
        'or_': [],
        'not_': [],
        'include_realms': [],
        'include_themes': ['some_theme'],
        'flags': [],
        'exclude_realms': [],
        'exclude_themes': [],
    }
    assert str(query) == '& some_theme'
