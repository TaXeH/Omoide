# -*- coding: utf-8 -*-

"""Actual search operations.
"""
import random
from typing import List, Dict, FrozenSet, Tuple

from omoide.application.search.class_query import Query


def random_records(amount: int, index_all: List[Tuple[int, str]]) -> List[str]:
    """"""
    # note that size of the repository in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(index_all))
    chosen_records = random.sample(index_all, adequate_amount)
    chosen_records.sort(key=lambda x: x[0])

    return [x[1] for x in chosen_records]


def find_records(query: Query, amount: int,
                 index_tags: Dict[str, FrozenSet[str]]) -> List[str]:
    """Return all records, that match to a given query."""
    # target_uuids = set()
    #
    # if query:
    #     for tag in chain(query.and_, query.or_):
    #         target_uuids.update(index_tags.get(tag, set()))
    # else:
    #     target_uuids = set()
    #
    # chosen_records = []

    # if constants.FLAG_DEMAND in query.flags:
    #     avoid_tags = set()
    # else:
    #     avoid_tags = set(theme.tags_on_demand) - query.and_ - query.or_

    # for uuid in target_uuids:
    #     meta = repository.get_record(uuid)
    #
    #     if meta is None:
    #         continue
    #
    #     tags = repository.get_extended_tags(meta.uuid)
    #
    #     if tags & avoid_tags:
    #         hidden += 1
    #         continue
    #
    #     # condition for and - all words must be present
    #     # condition for or - at least one word must be present
    #     # condition for not - no words must be present
    #     # skipped if predicate is empty
    #     cond_and_ = any((query.and_ & tags == query.and_,
    #                      len(query.and_) == 0))
    #
    #     cond_or_ = any((query.or_ & tags,
    #                     len(query.or_) == 0))
    #
    #     cond_not_ = any((not (query.not_ & tags),
    #                      len(query.not_) == 0))
    #
    #     if all((cond_and_, cond_or_, cond_not_)):
    #         chosen_records.append(meta)

    # if query.include:
    #     chosen_records = [
    #         x for x in chosen_records
    #         if x.directory in query.include
    #     ]

    # if query.exclude:
    #     chosen_records = [
    #         x for x in chosen_records
    #         if x.directory not in query.exclude
    #     ]

    # chosen_records.sort(key=core.core_utils.meta_sorter,
    #                     reverse=constants.FLAG_DESC in query.flags)
    uuids = set()

    for tag in query.and_:
        uuids.update(index_tags.get(tag, []))

    for tag in query.or_:
        uuids.update(index_tags.get(tag, []))

    for tag in query.not_:
        uuids = uuids - index_tags.get(tag, set())

    return list(uuids)
