# -*- coding: utf-8 -*-

"""Helper class that stores query parameters.
"""
import re
from typing import (
    TypeVar, Generic, Type, List, Dict, Set,
)

from omoide import constants
from omoide.utils import group_to_size

QueryType = TypeVar('QueryType')


class QueryBuilder(Generic[QueryType]):
    """Helper class that makes query instances.
    """
    string = '|'.join(
        r'(?<!\\)\{}'.format(x) for x in constants.OPERATORS
    )
    pattern = re.compile('(' + string + ')')

    search_map = {
        constants.KW_AND: 'and_',
        constants.KW_OR: 'or_',
        constants.KW_NOT: 'not_',
        constants.KW_FLAG: 'flags',
    }

    def __init__(self, target_type: Type[QueryType]) -> None:
        """Initialize instance."""
        self.target_type = target_type

    def split_request_into_parts(self, query_text: str) -> List[str]:
        """Turn user request into series of words."""
        parts = self.pattern.split(query_text)
        parts = [x.strip() for x in parts if x.strip()]

        if not parts:
            return []

        if parts[0] not in constants.OPERATORS:
            parts.insert(0, constants.KW_OR)

        return parts

    def update_sets(self, operator: str, word: str,
                    sets: Dict[str, Set[str]]) -> None:
        """Put new words in the sets dictionary."""
        if word not in constants.CASE_SENSITIVE:
            word = word.lower()

        target = self.search_map.get(operator, '')

        if target:
            sets[target].add(word)

    def from_query(self, query_text: str) -> QueryType:
        """Make instance representing given query."""
        sets = dict(and_=set(),
                    or_=set(),
                    not_=set(),
                    flags=set())

        parts = self.split_request_into_parts(query_text)

        for operator, word in group_to_size(parts):
            if not {operator, word} & constants.KEYWORDS:
                # something is wrong with this query
                # let's return object that can't be found
                return self.target_type(
                    and_={constants.NEVER_FIND_THIS},
                    or_=set(sets['or_']),
                    not_=set(sets['not_']),
                    flags=set(sets['flags']),
                )

            self.update_sets(operator, word, sets)

        return self.target_type(
            and_=set(sets['and_']),
            or_=set(sets['or_']),
            not_=set(sets['not_']),
            flags=set(sets['flags'])
        )
