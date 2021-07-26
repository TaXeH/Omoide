# -*- coding: utf-8 -*-

"""Tests.
"""
import pytest

from omoide import constants
from omoide.application.search.class_query import Query
from omoide.application.search.class_query_builder import QueryBuilder


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
        'flags': [],
    }


@pytest.fixture
def bad_query_dict():
    return {
        'and_': [constants.NEVER_FIND_THIS],
        'or_': ['cats'],
        'not_': [],
        'flags': [],
    }


def test_query_builder_split_query(query_builder):
    f = query_builder.split_request_into_parts
    assert f('cats | dogs') == ['|', 'cats', '|', 'dogs']
    assert f('a + b - c') == ['|', 'a', '+', 'b', '-', 'c']


def test_query_builder_1(query_builder):
    text = 'cats | dogs'
    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': [],
        'flags': [],
        'not_': [],
        'or_': ['cats', 'dogs'],
    }
    assert str(query) == '| cats | dogs'


def test_query_builder_2(query_builder):
    text = '+ cats | dogs + turtle - frog ~ image'

    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': ['cats', 'turtle'],
        'or_': ['dogs'],
        'not_': ['frog'],
        'flags': [constants.MEDIA_TYPE_IMAGE],
    }
    assert str(query) == '+ cats + turtle | dogs - frog ~ image'


def test_query_builder_3(query_builder):
    text = '|fly+fish-spiders~huge~audio'
    query = query_builder.from_query(text)
    assert query.as_dict() == {
        'and_': ['fish'],
        'or_': ['fly'],
        'not_': ['spiders'],
        'flags': ['audio', 'huge'],
    }
    assert str(query) == '+ fish | fly - spiders ~ audio ~ huge'


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
        'flags': ['demand', constants.FLAG_DESC],
    }
    assert str(query) == '+ other + some ~ demand ~ desc'
