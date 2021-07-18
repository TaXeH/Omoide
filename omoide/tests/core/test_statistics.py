# -*- coding: utf-8 -*-

"""Tests.
"""
from unittest.mock import ANY

import pytest

from omoide.essence.class_statistics import Statistics


@pytest.fixture
def statistics_fixture():
    inst = Statistics()
    inst.add('2021-10-01', 25, ['alpha', 'beta', 'gamma'])
    inst.add('2021-06-14', 250, ['alpha', 'cat', 'dog', 'fish'])
    inst.add('2021-02-28', 780, ['beta', 'home', 'ball', 'trust'])
    return inst


def test_statistics_creation(statistics_fixture):
    assert str(statistics_fixture) == '<Statistics, n=3>'


def test_statistics_as_dict(statistics_fixture):
    assert statistics_fixture.as_dict() == {
        'Newest item': '2021-10-01',
        'Oldest item': '2021-02-28',
        'Total items': '3',
        'Total size': '1.0 KiB',
        'Total tags': '9',
        'Tags by alphabet': ANY,
        'Tags by frequency': ANY
    }


def test_statistics_tags_by_frequency(statistics_fixture):
    assert statistics_fixture.tags_by_frequency == [
        ('alpha', 2),
        ('beta', 2),
        ('ball', 1),
        ('cat', 1),
        ('dog', 1),
        ('fish', 1),
        ('gamma', 1),
        ('home', 1),
        ('trust', 1),
    ]


def test_statistics_tags_by_alphabet(statistics_fixture):
    assert statistics_fixture.tags_by_alphabet == [
        ('A', ['alpha']),
        ('B', ['ball', 'beta']),
        ('C', ['cat']),
        ('D', ['dog']),
        ('F', ['fish']),
        ('G', ['gamma']),
        ('H', ['home']),
        ('T', ['trust']),
    ]


def test_statistics_iteration(statistics_fixture):
    assert list(statistics_fixture) == [
        ('Total items', '3'),
        ('Total size', '1.0 KiB'),
        ('Oldest item', '2021-02-28'),
        ('Newest item', '2021-10-01'),
        ('Total tags', '9'),
    ]


def test_statistics_sum(statistics_fixture):
    assert statistics_fixture.as_dict() == {
        'Newest item': '2021-10-01',
        'Oldest item': '2021-02-28',
        'Total items': '3',
        'Total size': '1.0 KiB',
        'Total tags': '9',
        'Tags by alphabet': [('A', ['alpha']),
                             ('B', ['ball', 'beta']),
                             ('C', ['cat']),
                             ('D', ['dog']),
                             ('F', ['fish']),
                             ('G', ['gamma']),
                             ('H', ['home']),
                             ('T', ['trust'])],
        'Tags by frequency': [('alpha', 2),
                              ('beta', 2),
                              ('ball', 1),
                              ('cat', 1),
                              ('dog', 1),
                              ('fish', 1),
                              ('gamma', 1),
                              ('home', 1),
                              ('trust', 1)]
    }

    assert (statistics_fixture
            + statistics_fixture
            + statistics_fixture).as_dict() == {
        'Newest item': '2021-10-01',
        'Oldest item': '2021-02-28',
        'Total items': '9',
        'Total size': '3.1 KiB',
        'Total tags': '9',
        'Tags by alphabet': [('A', ['alpha']),
                             ('B', ['ball', 'beta']),
                             ('C', ['cat']),
                             ('D', ['dog']),
                             ('F', ['fish']),
                             ('G', ['gamma']),
                             ('H', ['home']),
                             ('T', ['trust'])],
        'Tags by frequency': [('alpha', 6),
                              ('beta', 6),
                              ('ball', 3),
                              ('cat', 3),
                              ('dog', 3),
                              ('fish', 3),
                              ('gamma', 3),
                              ('home', 3),
                              ('trust', 3)],
    }


def test_statistics_not_implemented(statistics_fixture):
    with pytest.raises(TypeError):
        statistics_fixture + 25
