# -*- coding: utf-8 -*-

"""Actual search operations.
"""
import random
import time
from typing import List, Tuple

from omoide import utils
from omoide.search_engine.class_index import ShallowMeta, Index
from omoide.search_engine.class_query import Query


def random_records(index: Index, amount: int) -> List[ShallowMeta]:
    """Select random X records from index."""
    # note that size of the index in some cases might be smaller
    # than amount and random.sample will throw and exception
    adequate_amount = min(amount, len(index))
    chosen_records = random.sample(index.all_metas, adequate_amount)
    return chosen_records


def specific_records(query: Query, index: Index) \
        -> Tuple[List[ShallowMeta], List[str]]:
    """Return all records, that match to a given query."""
    target_uuids = index.all_uuids

    total = utils.sep_digits(len(target_uuids))
    report = [f'Found {total} records in index']

    # OR ----------------------------------------------------------------------

    if query.or_:
        or_start = time.perf_counter()
        temporary_or_ = set()
        for tag in query.or_:
            start = time.perf_counter()
            with_tag = index.get_by_tag(tag)
            if with_tag:
                temporary_or_ = temporary_or_.union(with_tag)
                duration = time.perf_counter() - start
                total = utils.sep_digits(len(with_tag))
                report.append('Found {} records '
                              'by tag {} in {:0.4f} sec.'.format(total,
                                                                 repr(tag),
                                                                 duration))
        if temporary_or_:
            target_uuids = target_uuids.intersection(temporary_or_)

        total = utils.sep_digits(len(target_uuids))
        duration = time.perf_counter() - or_start
        report.append(f'Got {total} records after OR in {duration:0.4f} sec.')

    # AND ---------------------------------------------------------------------

    if query.and_:
        and_start = time.perf_counter()
        for tag in query.and_:
            start = time.perf_counter()
            with_tag = index.get_by_tag(tag)
            target_uuids = target_uuids.intersection(with_tag)
            duration = time.perf_counter() - start
            total = utils.sep_digits(len(with_tag))
            report.append('Found {} records '
                          'by tag {} in {:0.4f} sec.'.format(total,
                                                             repr(tag),
                                                             duration))
        total = utils.sep_digits(len(target_uuids))
        duration = time.perf_counter() - and_start
        report.append(f'Got {total} records after AND in {duration:0.4f} sec.')

    # NOT ---------------------------------------------------------------------

    if query.not_:
        not_start = time.perf_counter()
        for tag in query.not_:
            start = time.perf_counter()
            with_tag = index.get_by_tag(tag)
            if with_tag:
                target_uuids -= with_tag
                duration = time.perf_counter() - start
                total = utils.sep_digits(len(with_tag))
                report.append('Found {} records '
                              'by tag {} in {:0.4f} sec.'.format(total,
                                                                 repr(tag),
                                                                 duration))
        total = utils.sep_digits(len(target_uuids))
        duration = time.perf_counter() - not_start
        report.append(f'Got {total} records after NOT in {duration:0.4f} sec.')

    # -------------------------------------------------------------------------

    sort_start = time.perf_counter()
    chosen_meta = [index.by_uuid[x] for x in target_uuids]
    chosen_meta.sort(key=lambda meta: meta.number)
    duration = time.perf_counter() - sort_start
    report.append(f'Complete sorting in {duration:0.4f} sec.')

    return chosen_meta, report
