# # -*- coding: utf-8 -*-
#
# """Tests.
# """
# import json
#
# import pytest
#
# from omoide import core
# from omoide.core import constants
# from omoide.use_cases.unite import preprocessing
#
#
# @pytest.fixture
# def source_text():
#     return """
# {
#     "aliases": {
#     },
#     "realms": [
#         {
#             "uuid": "$r_1",
#             "route": "test_realm",
#             "label": "Test realm",
#             "permissions": [
#                 "public"
#             ]
#         }
#     ],
#     "themes": [
#         {
#             "uuid": "$t_1",
#             "realm_uuid": "$r_1",
#             "route": "test_theme",
#             "label": "Test theme"
#         }
#     ],
#     "synonyms": [
#         {
#             "uuid": "$s_1",
#             "theme_uuid": "$t_1",
#             "description": "Test synonyms",
#             "values": [
#                 "one",
#                 "two",
#                 "three"
#             ]
#         }
#     ],
#     "implicit_tags": [
#         {
#             "uuid": "$i_1",
#             "theme_uuid": "$t_1",
#             "description": "Test implicit tags",
#             "values": [
#                 "four"
#             ]
#         }
#     ],
#     "groups": [
#         {
#             "uuid": "$g_1",
#             "realm_uuid": "$r_1",
#             "theme_uuid": "$t_1",
#             "route": "test_group",
#             "label": "Test group",
#             "registered_on": "$today",
#             "path": "./path"
#         }
#     ],
#     "metas": [
#         {
#             "realm_uuid": "$r_1",
#             "theme_uuid": "$t_1",
#             "registered_on": "$today",
#             "path": "./folder"
#         }
#     ],
#     "users": [
#         {
#             "uuid": "$u_1",
#             "login": "supersexy1975"
#         }
#     ]
# }
#     """
#
#
# def test_preprocessing_apply_variables(source_text):
#     uuid_master = core.UUIDMaster()
#     uuid_master.generate_uuid4 = lambda: 'generated'
#     output = preprocessing.apply_variables(source_text, uuid_master)
#     as_dict = json.loads(output)
#
#     assert as_dict['synonyms'][0]['uuid'] == 's_generated'
#     assert as_dict['implicit_tags'][0]['uuid'] == 'i_generated'
#     assert as_dict['groups'][0]['uuid'] == 'g_generated'
#     assert as_dict['users'][0]['uuid'] == 'u_generated'
#
#
# def test_preprocessing_apply_aliases(source_text):
#     as_dict = json.loads(source_text)
#     as_dict['aliases'] = {'r_1': 'r_var1', 't_1': 't_var2'}
#     source_text = json.dumps(as_dict)
#
#     uuid_master = core.UUIDMaster(aliases=as_dict['aliases'])
#     uuid_master.generate_uuid4 = lambda: 'generated'
#     output = preprocessing.apply_variables(source_text, uuid_master)
#     as_dict = json.loads(output)
#
#     assert as_dict['realms'][0]['uuid'] == 'r_var1'
#     assert as_dict['themes'][0]['uuid'] == 't_var2'
#     assert as_dict['metas'][0]['realm_uuid'] == 'r_var1'
#     assert as_dict['metas'][0]['theme_uuid'] == 't_var2'
#
#
# def test_preprocessing_apply_global_variables(source_text):
#     ref = '2021-01-01'
#
#     output = preprocessing.apply_global_variables(source_text, today=ref)
#     as_dict = json.loads(output)
#
#     assert as_dict['groups'][0]['registered_on'] == ref
#     assert as_dict['metas'][0]['registered_on'] == ref
#
#
# def test_preprocess_source(source_text):
#     uuid_master = core.UUIDMaster()
#     uuid_master.generate_uuid4 = lambda: 'generated'
#     output = preprocessing.preprocess_source(source_text, uuid_master)
#
#     assert core.constants.VARIABLE_SIGN not in output
#
#
# def test_preprocessing_variable_cache(source_text):
#     ref_uuids = [
#         'r_generated',
#         't_generated',
#         'g_generated',
#         's_generated',
#         'i_generated',
#         'u_generated',
#     ]
#     uuid_master = core.UUIDMaster()
#     uuid_master.generate_uuid4 = lambda: 'generated'
#
#     for uuid in ref_uuids:
#         assert uuid not in uuid_master
#
#     preprocessing.preprocess_source(source_text, uuid_master)
#
#     for uuid in ref_uuids:
#         assert uuid in uuid_master
