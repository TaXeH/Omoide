# # -*- coding: utf-8 -*-
#
# """Class for search enhancement.
# """
# from functools import lru_cache
# from typing import Set, List
#
# from omoide.core.class_group import Group
# from omoide.core.class_meta import Meta
#
# import omoide.constants
# from omoide.core.class_synonym import Synonym
# from omoide.core import constants
#
#
# def get_extended_tags(group: Group, meta: Meta) -> Set[str]:
#     """Get base tags with additional words for search."""
#     collection = {
#         *(tag.lower() for tag in meta.tags),
#         *(tag.lower() for tag in group.tags),
#         *(key.lower() for key in group.hierarchy),
#         meta.uuid,
#         meta.author,
#         group.label,
#         get_image_size_tag(meta.resolution),
#         get_duration_tag(meta.duration),
#         get_media_type_tag(meta.type),
#     }
#     return set(filter(None, collection))
#
#
# def get_extended_tags_with_synonyms(group: Group,
#                                     meta: Meta,
#                                     synonyms: List[Synonym]) -> Set[str]:
#     """Get extended tags + synonyms for search."""
#     base_tags = get_extended_tags(group, meta)
#     additional_tags = set()
#
#     for each_set in synonyms:
#         for tag in base_tags:
#             if tag in each_set:
#                 additional_tags.update(each_set)
#                 continue
#
#     return base_tags | additional_tags
#
#
# @lru_cache()
# def get_image_size_tag(resolution: float) -> str:
#     """Get textual identifier for image size."""
#     cls_t = constants.ImageResolutionThreshold
#     cls_v = constants.ImageResolutionMpx
#
#     if 0 < resolution < cls_t.THRESHOLD_TINY.value:
#         return cls_v.RESOLUTION_TINY.value
#
#     if cls_t.THRESHOLD_TINY.value <= resolution < cls_t.THRESHOLD_SMALL.value:
#         return cls_v.RESOLUTION_SMALL.value
#
#     if cls_t.THRESHOLD_SMALL.value <= resolution < cls_t.THRESHOLD_MEAN.value:
#         return cls_v.RESOLUTION_MEAN.value
#
#     if cls_t.THRESHOLD_MEAN.value <= resolution < cls_t.THRESHOLD_BIG.value:
#         return cls_v.RESOLUTION_BIG.value
#
#     if resolution >= cls_t.THRESHOLD_BIG.value:
#         return cls_v.RESOLUTION_HUGE.value
#
#     return omoide.constants.UNKNOWN
#
#
# @lru_cache()
# def get_duration_tag(seconds: int) -> str:
#     """Get textual identifier for media length."""
#     cls_t = constants.DurationThreshold
#     cls_v = constants.MediaDuration
#
#     if 0 < seconds < cls_t.THRESHOLD_MOMENT.value:
#         return cls_v.DURATION_MOMENT.value
#
#     if cls_t.THRESHOLD_MOMENT.value <= seconds < cls_t.THRESHOLD_SHORT.value:
#         return cls_v.DURATION_SHORT.value
#
#     if cls_t.THRESHOLD_SHORT.value <= seconds < cls_t.THRESHOLD_MEDIUM.value:
#         return cls_v.DURATION_MEDIUM.value
#
#     if seconds >= cls_t.THRESHOLD_MEDIUM.value:
#         return cls_v.DURATION_LONG.value
#
#     return omoide.constants.UNKNOWN
#
#
# @lru_cache()
# def get_media_type_tag(media_type: str) -> str:
#     """Get textual identifier for media type."""
#     return {
#         'image': constants.MediaType.TYPE_IMAGE,
#         'gif': constants.MediaType.TYPE_GIF,
#         'video': constants.MediaType.TYPE_VIDEO,
#         'audio': constants.MediaType.TYPE_AUDIO,
#     }.get(media_type, omoide.constants.UNKNOWN)
