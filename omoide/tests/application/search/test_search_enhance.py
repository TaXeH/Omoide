# # -*- coding: utf-8 -*-
#
# """Tests.
# """
# import random
#
# from omoide.core.class_group import Group
# from omoide.core.class_meta import Meta
# from omoide.core.class_synonym import Synonym
# from omoide.core import constants
# from omoide.core.search.search_enhance import (
#     get_extended_tags, get_extended_tags_with_synonyms,
#     get_image_size_tag, get_duration_tag,
# )
#
#
# def test_search_enhancer_get_extended_tags():
#     synonyms = Synonym([['red', 'green'], ['smaller', 'little']])
#     meta = Meta(tags=['red'])
#     group = Group(hierarchy=['smaller', 'bigger'])
#
#     assert get_extended_tags(group, meta) == {
#         'bigger',
#         'red',
#         'UNKNOWN',
#         'smaller',
#     }
#
#     assert get_extended_tags_with_synonyms(group, meta, synonyms) == {
#         'green',
#         'UNKNOWN',
#         'red',
#         'smaller',
#         'bigger',
#         'little',
#     }
#
#
# def test_get_image_size_tag():
#     cls_t = constants.ImageResolutionThreshold
#     cls_v = constants.ImageResolutionMpx
#
#     tiny = random.randint(
#         1,
#         int(cls_t.THRESHOLD_TINY.value * 1000) - 1
#     ) / 1000
#     assert get_image_size_tag(tiny) == cls_v.RESOLUTION_TINY.value
#
#     small = random.randint(
#         int(cls_t.THRESHOLD_TINY.value * 1000),
#         int(cls_t.THRESHOLD_SMALL.value * 1000) - 1
#     ) / 1000
#     assert get_image_size_tag(small) == cls_v.RESOLUTION_SMALL.value
#
#     mean = random.randint(
#         int(cls_t.THRESHOLD_SMALL.value * 1000),
#         int(cls_t.THRESHOLD_MEAN.value * 1000) - 1
#     ) / 1000
#     assert get_image_size_tag(mean) == cls_v.RESOLUTION_MEAN.value
#
#     big = random.randint(
#         int(cls_t.THRESHOLD_MEAN.value * 1000),
#         int(cls_t.THRESHOLD_BIG.value * 1000) - 1
#     ) / 1000
#     assert get_image_size_tag(big) == cls_v.RESOLUTION_BIG.value
#
#     huge = random.randint(
#         int(cls_t.THRESHOLD_BIG.value * 1000),
#         int(cls_t.THRESHOLD_BIG.value * 1000) + 1
#     ) / 1000
#     assert get_image_size_tag(huge) == cls_v.RESOLUTION_HUGE.value
#
#
# def test_get_duration_tag():
#     cls_t = constants.DurationThreshold
#     cls_v = constants.MediaDuration
#
#     moment = random.randint(
#         1,
#         int(cls_t.THRESHOLD_MOMENT.value) - 1
#     )
#     assert get_duration_tag(moment) == cls_v.DURATION_MOMENT.value
#
#     short = random.randint(
#         int(cls_t.THRESHOLD_MOMENT.value),
#         int(cls_t.THRESHOLD_SHORT.value) - 1
#     )
#     assert get_duration_tag(short) == cls_v.DURATION_SHORT.value
#
#     medium = random.randint(
#         int(cls_t.THRESHOLD_SHORT.value),
#         int(cls_t.THRESHOLD_MEDIUM.value) - 1
#     )
#     assert get_duration_tag(medium) == cls_v.DURATION_MEDIUM.value
#
#     long = random.randint(
#         int(cls_t.THRESHOLD_MEDIUM.value),
#         int(cls_t.THRESHOLD_MEDIUM.value) + 1
#     )
#     assert get_duration_tag(long) == cls_v.DURATION_LONG.value
