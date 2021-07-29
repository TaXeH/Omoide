# -*- coding: utf-8 -*-
"""Fast lookup values, some statistic, etc.
"""
import json

from sqlalchemy.orm import Session

from omoide import infra, constants
from omoide.database import models
from omoide.migration_engine.classes import class_statistics


def build_helpers(session: Session, stdout: infra.STDOut) -> int:
    """Create fast lookup tables."""
    new_values = 0
    new_values += calculate_statistics(session, stdout)
    new_values += construct_entities_graph(session, stdout)
    return new_values


def calculate_statistics(session: Session, stdout: infra.STDOut) -> int:
    """Calculate statistics for all realms/themes."""
    stdout.print('\tCalculating statistics')
    new_values = 0

    all_realm_stats = class_statistics.Statistics()
    for realm in session.query(models.Realm).all():
        realm_stats = class_statistics.Statistics()
        for theme in realm.themes:
            theme_stats = class_statistics.Statistics()
            for group in theme.groups:
                for meta in group.metas:
                    theme_stats.add(
                        item_date=meta.registered_on,
                        item_size=meta.size,
                        item_tags=[x.value for x in meta.tags]
                    )

            realm_stats += theme_stats
            new_helper = models.Helper(
                key=f'stats__{realm.uuid}__{theme.uuid}',
                value=json.dumps(theme_stats.as_dict(), ensure_ascii=False)
            )
            session.add(new_helper)
            new_values += 1

        new_helper = models.Helper(
            key=f'stats__{realm.uuid}__{constants.ALL_THEMES}',
            value=json.dumps(realm_stats.as_dict(), ensure_ascii=False)
        )
        session.add(new_helper)
        new_values += 1
        all_realm_stats += realm_stats

    new_helper = models.Helper(
        key=f'stats__{constants.ALL_REALMS}__{constants.ALL_THEMES}',
        value=json.dumps(all_realm_stats.as_dict(), ensure_ascii=False)
    )
    session.add(new_helper)
    new_values += 1

    session.commit()
    return new_values


def construct_entities_graph(session: Session, stdout: infra.STDOut) -> int:
    """Build graph of available realms/themes."""
    stdout.print('\tConstructing graph')
    # TODO - we're ignoring the fact that
    #  server can have private realms for now
    graph = {}
    for realm in session.query(models.Realm).all():
        sub_graph = {}
        for theme in realm.themes:
            sub_graph[theme.uuid] = {
                'uuid': theme.uuid,
                'label': theme.label,
                'groups': sorted(x.label for x in theme.groups)
            }

        graph[realm.uuid] = {
            'uuid': realm.uuid,
            'label': realm.label,
            'themes': sub_graph
        }

    new_helper = models.Helper(
        key='graph',
        value=json.dumps(graph, ensure_ascii=False)
    )

    session.add(new_helper)
    session.commit()

    return 1
