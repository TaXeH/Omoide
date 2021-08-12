# -*- coding: utf-8 -*-

"""Actual search operations.
"""
import random
from typing import List

from omoide.application.search.class_index import ShallowMeta, Index
from omoide.application.search.class_query import Query


def random_records(index: Index, amount: int) -> List[ShallowMeta]:
    """Select random X records from index."""
    # note that size of the index in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(index))
    chosen_records = random.sample(index.all_metas, adequate_amount)
    return chosen_records


def find_records(query: Query, index: Index) -> List[ShallowMeta]:
    """Return all records, that match to a given query."""
    # print(query)
    target_uuids = index.all_uuids
    # print(1, len(target_uuids), target_uuids)
    or_ = set()
    for tag in query.or_:
        with_tag = index.get_by_tag(tag)
        # print('performing or', tag, len(with_tag), with_tag)
        or_ = or_.union(with_tag)
    # print(2, len(target_uuids), target_uuids)

    if or_ or query.or_:
        target_uuids = target_uuids.intersection(or_)
    # print(3, len(target_uuids), target_uuids)

    for tag in query.and_:
        with_tag = index.get_by_tag(tag)
        # print('performing and', tag, len(with_tag), with_tag)
        target_uuids = target_uuids.intersection(with_tag)
    # print(4, len(target_uuids), target_uuids)

    for tag in query.not_:
        with_tag = index.get_by_tag(tag)
        # print('performing not', tag, len(with_tag), with_tag)
        target_uuids -= with_tag

    # print(5, len(target_uuids), target_uuids)

    chosen_meta = [index.by_uuid[x] for x in target_uuids]
    chosen_meta.sort(key=lambda meta: meta.number)

    return chosen_meta
