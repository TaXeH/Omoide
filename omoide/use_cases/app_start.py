# -*- coding: utf-8 -*-

"""Initial loading and building for the indexes.
"""
from dataclasses import dataclass
from typing import List, Callable, Dict

import omoide.database.models.base
from omoide.core.class_group import Group
from omoide.core.class_meta import Meta
from omoide.core.class_realm import Realm
from omoide.core.class_statistics import Statistics
from omoide.core.class_synonym import Synonym
from omoide.core.class_theme import Theme
from omoide.core.search.class_index import Index, IndexItem
from omoide.core.search.search_enhance import get_extended_tags_with_synonyms
from omoide.core.search.search_routine import finalize_metarecord


@dataclass
class Storage:
    """Keeper of the state."""
    realms: Dict[str, Realm]
    themes: Dict[str, Theme]
    groups: Dict[str, Group]
    statistics: Dict[str, Statistics]


def app_start(realms: List[Realm], themes: [Theme],
              groups: List[Group], metas: List[Meta]) -> Storage:
    """Full pledged initial loading."""
    realms_map = {realm.uuid: realm for realm in realms}
    themes_map = {theme.uuid: theme for theme in themes}
    groups_map = {group.uuid: group for group in groups}
    synonyms_map = {}
    statistics_map = {}

    def get_or_create(key: str, storage: dict, callback: Callable):
        """Shorthand for extraction of items."""
        value = storage.get(key)
        if value is not None:
            return value
        value = callback()
        storage[key] = value
        return value

    meta_index = Index()
    realm_index = Index()
    theme_index = Index()
    all_metas = []

    for meta in metas:
        realm = realms_map[meta.realm_uuid]
        theme = themes_map[meta.theme_uuid]
        group = groups_map[meta.group_uuid]
        bigger_meta = finalize_metarecord(realm, theme, group, meta)
        all_metas.append(bigger_meta)

        realm_index.add(meta.realm_uuid, IndexItem(theme.uuid))
        theme_index.add(meta.theme_uuid, IndexItem(group.uuid))

        synonyms = get_or_create(
            theme.uuid, synonyms_map,
            lambda: Synonym(
                omoide.database.models.base.synonyms.values()))

        stat_kwargs = dict(item_date=bigger_meta.registered_on,
                           item_size=bigger_meta.size,
                           item_tags=bigger_meta.tags)

        statistics = get_or_create(realm.uuid, statistics_map, Statistics)
        statistics.add(**stat_kwargs)

        statistics = get_or_create(theme.uuid, statistics_map, Statistics)
        statistics.add(**stat_kwargs)

        extended_tags = get_extended_tags_with_synonyms(group,
                                                        bigger_meta,
                                                        synonyms)
        for tag in extended_tags:
            meta_index.add(tag,
                           IndexItem(uuid=bigger_meta.uuid,
                                     payload=bigger_meta.path_to_thumbnail))

    synonyms_map.clear()

    def meta_sorter(_meta: Meta) -> tuple:
        """Metarecord sorting function."""
        realm = realms_map[_meta.realm_uuid]
        theme = themes_map[_meta.theme_uuid]
        group = groups_map[_meta.group_uuid]
        string = ','.join(x.strip() for x in group.hierarchy)
        return (
            realm.label,
            theme.label,
            group.label,
            string,
            _meta.ordering
        )

    all_metas.sort(key=meta_sorter)
    for i, meta in enumerate(all_metas):
        meta.ordering = i

    return Storage(
        realms=realms_map,
        themes=themes_map,
        groups=groups_map,
        statistics=statistics_map,
    )
