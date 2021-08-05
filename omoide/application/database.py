import json
from collections import defaultdict
from typing import Optional

from sqlalchemy.orm import Session

from omoide import constants
from omoide.application.search.class_index import ShallowMeta, Index
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


def get_index(session: Session) -> Index:
    metas = list(session.query(models.IndexMetas).order_by('number').all())
    all_metas = [
        ShallowMeta(x.meta_uuid, x.number, x.path_to_thumbnail)
        for x in metas
    ]

    by_tags = defaultdict(set)
    for each in session.query(models.IndexTags).all():
        by_tags[each.tag].add(each.uuid)

    by_permissions = defaultdict(set)
    for each in session.query(models.IndexPermissions).all():
        by_permissions[each.permission].add(each.uuid)

    index = Index(
        all_metas=all_metas,
        by_tags={
            tag: frozenset(uuids)
            for tag, uuids in by_tags.items()
        },
        by_permission={
            permission: frozenset(uuids)
            for permission, uuids in by_permissions.items()
        },
    )

    return index


def get_graph(session: Session) -> dict:
    # text = session.query(models.Helper).where(
    #     models.Helper.key == 'graph').one().value
    txt = """
{
    "A": {
        "label": "Basic",
        "elements": {
            "A-1": {
                "label": "Mice and humans",
                "elements": {
                    "A-1-1": {
                        "label": "History"
                    },
                    "A-1-2": {
                        "label": "As pets"
                    },
                    "A-1-3": {
                        "label": "As model organism"
                    },
                    "A-1-4": {
                        "label": "Folk culture"
                    }
                }
            },
            "A-2": {
                "label": "Life expectancy"
            },
            "A-3": {
                "label": "Life cycle and reproduction",
                "elements": {
                    "A-3-1": {
                        "label": "Polygamy"
                    },
                    "A-3-2": {
                        "label": "Polyandry"
                    }
                }
            }
        }
    },
    "B": {
        "label": "Animalia"
    },
    "C": {
        "label": "Senses",
        "elements": {
            "C-1": {
                "label": "Vision"
            },
            "C-2": {
                "label": "Olfaction"
            },
            "C-3": {
                "label": "Tactile"
            }
        }
    },
    "D": {
        "label": "Behavior",
        "elements": {
            "D-1": {
                "label": "Social behavior"
            }
        }
    }
}    
    """
    return json.loads(txt)  #FIXME


def get_stats(session: Session, current_realm: str,
              current_theme: str) -> dict:
    key = f'stats__{current_realm}__{current_theme}'
    item = session.query(models.Helper).where(
        models.Helper.key == key).first()
    if item is None:
        return {}

    return json.loads(item.value)
