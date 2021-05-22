# -*- coding: utf-8 -*-

"""Tests.
"""

import pytest

from omoide import core


@pytest.fixture
def uuid_master_1():
    return core.UUIDMaster(
        aliases={'r_5': 'r_other'},
        uuids_realms=['r_1', 'r_2', 'r_3'],
        uuids_themes=['t_1', 't_2', 't_3'],
        uuids_groups=['g_1', 'g_2', 'g_3'],
        uuids_metas=['m_1', 'm_2', 'm_3'],
        uuids_synonyms=['s_1', 's_2', 's_3'],
        uuids_implicit_tags=['i_1', 'i_2', 'i_3'],
        uuids_users=['u_1', 'u_2', 'u_3'],
    )


@pytest.fixture
def uuid_master_2():
    return core.UUIDMaster(
        aliases={'r_7': 'r_word'},
        uuids_realms=['r_9', 'r_10', 'r_11'],
        uuids_themes=['t_9', 't_10', 't_11'],
        uuids_groups=['g_9', 'g_10', 'g_11'],
        uuids_metas=['m_9', 'm_10', 'm_11'],
        uuids_synonyms=['s_9', 's_10', 's_11'],
        uuids_implicit_tags=['i_9', 'i_10', 'i_11'],
        uuids_users=['u_9', 'u_10', 'u_11'],
    )


def test_uuid_master_add(uuid_master_1, uuid_master_2):
    res = uuid_master_1 + uuid_master_2

    assert isinstance(res, core.UUIDMaster)
    assert res.aliases == {'r_5': 'r_other', 'r_7': 'r_word'}
    assert res.uuids_realms == {'r_11', 'r_3', 'r_word', 'r_2',
                                'r_other', 'r_1', 'r_9', 'r_10'}
    assert res.uuids_themes == {'t_1', 't_10', 't_2', 't_11', 't_3', 't_9'}
    assert res.uuids_groups == {'g_11', 'g_3', 'g_10', 'g_2', 'g_9', 'g_1'}
    assert res.uuids_metas == {'m_11', 'm_3', 'm_10', 'm_2', 'm_9', 'm_1'}
    assert res.uuids_synonyms == {'s_9', 's_2', 's_1', 's_11', 's_10', 's_3'}
    assert res.uuids_implicit_tags == {'i_9', 'i_2', 'i_1',
                                       'i_10', 'i_11', 'i_3'}
    assert res.uuids_users == {'u_10', 'u_3', 'u_11', 'u_2', 'u_9', 'u_1'}


def test_uuid_master_iadd(uuid_master_1, uuid_master_2):
    uuid_master_1 += uuid_master_2
    res = uuid_master_1

    assert isinstance(res, core.UUIDMaster)
    assert res.aliases == {'r_5': 'r_other', 'r_7': 'r_word'}
    assert res.uuids_realms == {'r_11', 'r_3', 'r_word', 'r_2',
                                'r_other', 'r_1', 'r_9', 'r_10'}
    assert res.uuids_themes == {'t_1', 't_10', 't_2', 't_11', 't_3', 't_9'}
    assert res.uuids_groups == {'g_11', 'g_3', 'g_10', 'g_2', 'g_9', 'g_1'}
    assert res.uuids_metas == {'m_11', 'm_3', 'm_10', 'm_2', 'm_9', 'm_1'}
    assert res.uuids_synonyms == {'s_9', 's_2', 's_1', 's_11', 's_10', 's_3'}
    assert res.uuids_implicit_tags == {'i_9', 'i_2', 'i_1',
                                       'i_10', 'i_11', 'i_3'}
    assert res.uuids_users == {'u_10', 'u_3', 'u_11', 'u_2', 'u_9', 'u_1'}
