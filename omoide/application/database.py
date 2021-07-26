from collections import defaultdict
from typing import Optional, FrozenSet, Dict, Tuple, List

from sqlalchemy.orm import Session

from omoide import constants
from omoide.database import models


def get_realm_uuid(session: Session,
                   realm_route: str) -> Optional[str]:
    if realm_route == constants.ALL_REALMS:
        return realm_route

    realm = session.query(models.Realm) \
        .where(models.Realm.route == realm_route).first()

    if realm is None:
        return None

    return realm.uuid


def get_theme_uuid(session: Session,
                   theme_route: str) -> Optional[str]:
    if theme_route == constants.ALL_THEMES:
        return theme_route

    theme = session.query(models.Theme) \
        .where(models.Theme.route == theme_route).first()

    if theme is None:
        return None

    return theme.uuid


def get_group_uuid(session: Session,
                   group_route: str) -> Optional[str]:
    if group_route == constants.ALL_GROUPS:
        return group_route

    group = session.query(models.Group) \
        .where(models.Group.route == group_route).first()

    if group is None:
        return None

    return group.uuid


def get_meta(session: Session,
             meta_uuid: str):
    return session.query(models.Meta) \
        .where(models.Meta.uuid == meta_uuid).one()


def get_all_metas(session: Session):
    return session.query(models.Meta).all()


def get_index_thumbnails(session: Session) -> Dict[str, str]:
    index = {}
    for each in session.query(models.IndexThumbnails).all():
        index[each.meta_uuid] = each.path_to_thumbnail
    return index


def get_index_tags(session: Session) -> Dict[str, FrozenSet[str]]:
    index = defaultdict(set)
    for each in session.query(models.IndexTags).all():
        index[each.tag].add(each.uuid)
    return {tag: frozenset(uuids) for tag, uuids in index.items()}


def get_index_all(session: Session) -> List[Tuple[int, str]]:
    all_uuids = []
    for i, meta in enumerate(session.query(models.Meta).all()):
        all_uuids.append((i, meta.uuid))
    return all_uuids
