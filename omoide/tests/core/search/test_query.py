# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from omoide.vision.search.class_query import Query


@pytest.fixture
def query():
    inst = Query(
        and_=frozenset(['and_this', 'and_that']),
        or_=frozenset(['or_this', 'or_that']),
        not_=frozenset(['not_this']),
        flags=frozenset(['wtf']),
    )
    return inst


@pytest.fixture
def empty_query():
    inst = Query(
        and_=frozenset(),
        or_=frozenset(),
        not_=frozenset(),
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
                               'flags': ['wtf'],
                               'not_': ['not_this'],
                               'or_': ['or_that', 'or_this']}

    assert empty_query.as_dict() == {'and_': [],
                                     'flags': [],
                                     'not_': [],
                                     'or_': []}


def test_query_as_keywords(query, empty_query):
    assert query.as_keywords() == {'and_': ['+ and_that', '+ and_this'],
                                   'flags': ['~ wtf'],
                                   'not_': ['- not_this'],
                                   'or_': ['| or_that', '| or_this']}

    assert empty_query.as_keywords() == {'and_': [],
                                         'flags': [],
                                         'not_': [],
                                         'or_': []}


def test_query_repr(query, empty_query):
    assert repr(query) == '<Query, n=6>'
    assert repr(empty_query) == '<Query, n=0>'


def test_query_str(query, empty_query):
    assert str(query) == (
        '+ and_that + and_this | or_that | or_this - not_this ~ wtf'
    )
    assert str(empty_query) == ''
