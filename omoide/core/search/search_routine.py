# -*- coding: utf-8 -*-

"""Actual search operations.
"""
from omoide.core.class_group import Group
from omoide.core.class_meta import Meta
from omoide.core.class_realm import Realm
from omoide.core.class_theme import Theme


def finalize_metarecord(realm: Realm, theme: Theme,
                        group: Group, meta: Meta) -> Meta:
    """Make fully extended instance of metarecord.

    Kind of inheritance. New metarecord takes
    permissions and other parameters from super entities.
    """
    sentinel = object()

    def take_first(attr: str, *args):
        """Return first not empty value."""
        for each in args:
            value = getattr(each, attr, sentinel)
            if value is not sentinel and value:
                break
        else:
            raise RuntimeError('No args supplied')
        return value

    return Meta(
        uuid=meta.uuid,
        realm_uuid=realm.uuid,
        theme_uuid=theme.uuid,
        group_uuid=group.uuid,
        path_to_content=meta.path_to_content,
        path_to_preview=meta.path_to_preview,
        path_to_thumbnail=meta.path_to_thumbnail,
        original_filename=meta.original_filename,
        original_extension=meta.original_extension,
        width=meta.width,
        height=meta.height,
        resolution=meta.resolution,
        size=meta.size,
        duration=meta.duration,
        type=meta.type,
        ordering=meta.ordering,
        registered_on=take_first('registered_on', meta, group),
        registered_by=take_first('registered_by', meta, group),
        author=take_first('author', meta, group),
        author_url=take_first('author_url', meta, group),
        origin_url=take_first('origin_url', meta, group),
        comment=take_first('comment', meta, group),
        signature=meta.signature,
        signature_type=meta.signature_type,
        tags=meta.tags + group.tags,
        permissions=(realm.permissions + theme.permissions
                     + group.permissions + meta.permissions),
    )


def find_random_records():
    """"""
    # FIXME
    pass


def find_records():
    """"""
    # FIXME
    pass
