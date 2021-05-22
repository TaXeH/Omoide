# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from omoide.core.search.class_query import Query


@pytest.fixture
def query():
    inst = Query(
        and_=frozenset(['and_this', 'and_that']),
        or_=frozenset(['or_this', 'or_that']),
        not_=frozenset(['not_this']),
        include_realms=frozenset(['admin']),
        exclude_realms=frozenset(['user']),
        include_themes=frozenset(['cabbage']),
        exclude_themes=frozenset(['pie']),
        flags=frozenset(['wtf']),
    )
    return inst


@pytest.fixture
def empty_query():
    inst = Query(
        and_=frozenset(),
        or_=frozenset(),
        not_=frozenset(['not_this']),
        include_realms=frozenset(['admin']),
        exclude_realms=frozenset(['user']),
        include_themes=frozenset(['cabbage']),
        exclude_themes=frozenset(['pie']),
        flags=frozenset(),
    )
    return inst


def test_query_contains(query, empty_query):
    assert 'and_this' in query.and_
    assert 'unknown' not in empty_query.or_

    assert query
    assert not empty_query


def test_query_as_dict(query, empty_query):
    assert query.as_dict() == {'and_': ['and_that', 'and_this'],
                               'exclude_realms': ['user'],
                               'exclude_themes': ['pie'],
                               'flags': ['wtf'],
                               'include_realms': ['admin'],
                               'include_themes': ['cabbage'],
                               'not_': ['not_this'],
                               'or_': ['or_that', 'or_this']}

    assert empty_query.as_dict() == {'and_': [],
                                     'exclude_realms': ['user'],
                                     'exclude_themes': ['pie'],
                                     'flags': [],
                                     'include_realms': ['admin'],
                                     'include_themes': ['cabbage'],
                                     'not_': ['not_this'],
                                     'or_': []}


def test_query_as_keywords(query, empty_query):
    assert query.as_keywords() == {'and_': ['+ and_that', '+ and_this'],
                                   'exclude_realms': ['!! user'],
                                   'exclude_themes': ['! pie'],
                                   'flags': ['~ wtf'],
                                   'include_realms': ['&& admin'],
                                   'include_themes': ['& cabbage'],
                                   'not_': ['- not_this'],
                                   'or_': ['| or_that', '| or_this']}

    assert empty_query.as_keywords() == {'and_': [],
                                         'exclude_realms': ['!! user'],
                                         'exclude_themes': ['! pie'],
                                         'flags': [],
                                         'include_realms': ['&& admin'],
                                         'include_themes': ['& cabbage'],
                                         'not_': ['- not_this'],
                                         'or_': []}


def test_query_repr(query, empty_query):
    assert repr(query) == '<Query, n=10>'
    assert repr(empty_query) == '<Query, n=5>'


def test_query_str(query, empty_query):
    assert str(query) == (
        '+ and_that + and_this | or_that | or_this '
        '- not_this && admin !! user & cabbage ! pie ~ wtf'
    )

    assert str(empty_query) == '- not_this && admin !! user & cabbage ! pie'
