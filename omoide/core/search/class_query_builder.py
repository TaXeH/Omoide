# -*- coding: utf-8 -*-

"""Helper class that stores query parameters.
"""
import re
from itertools import zip_longest
from typing import (
    TypeVar, Generic, Type, List, Dict,
    Set, Iterable, Any, Iterator,
)

from omoide.core import constants

QueryType = TypeVar('QueryType')


def group_to_size(iterable: Iterable, group_size: int = 2,
                  default: Any = '?') -> Iterator[tuple]:
    """Return contents of the iterable grouped in blocks of given size.

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 2, '?'))
    [(1, 2), (3, 4), (5, 6), (7, '?')]

    >>> list(group_to_size([1, 2, 3, 4, 5, 6, 7], 3, '?'))
    [(1, 2, 3), (4, 5, 6), (7, '?', '?')]
    """
    return zip_longest(*[iter(iterable)] * group_size, fillvalue=default)


class QueryBuilder(Generic[QueryType]):
    """Helper class that makes query instances.
    """
    string = '|'.join(
        r'(?<!\\)\{}'.format(x.value)
        for x in constants.Operators.__members__.values()
    )
    pattern = re.compile('(' + string + ')')

    search_map = {
        constants.Operators.KW_AND.value: 'and_',
        constants.Operators.KW_OR.value: 'or_',
        constants.Operators.KW_NOT.value: 'not_',
        constants.Operators.KW_FLAG.value: 'flags',
        constants.Operators.KW_INCLUDE_R.value: 'include_realms',
        constants.Operators.KW_EXCLUDE_R.value: 'exclude_realms',
        constants.Operators.KW_INCLUDE_T.value: 'include_themes',
        constants.Operators.KW_EXCLUDE_T.value: 'exclude_themes',
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

        if parts[0] not in constants.Operators.tokens():
            parts.insert(0, constants.Operators.KW_OR.value)

        return parts

    def update_sets(self, operator: str, word: str,
                    sets: Dict[str, Set[str]]) -> None:
        """Put new words in the sets dictionary."""
        if word not in constants.CASE_SENSITIVE:
            word = word.lower()

        target = self.search_map.get(operator, '')

        if target:
            sets[target].add(word)

    def from_query(self, query_text: str, current_realm: str = '',
                   current_theme: str = '') -> QueryType:
        """Make instance representing given query."""
        sets = dict(and_=set(),
                    or_=set(),
                    not_=set(),
                    include_realms=set(),
                    exclude_realms=set(),
                    include_themes=set(),
                    exclude_themes=set(),
                    flags=set())

        parts = self.split_request_into_parts(query_text)

        if current_realm and current_realm != constants.ALL_REALMS:
            sets['include_realms'].add(current_realm)

        if current_theme and current_theme != constants.ALL_THEMES:
            sets['include_themes'].add(current_theme)

        for operator, word in group_to_size(parts):
            if not {operator, word} & constants.KEYWORDS:
                # something is wrong with this query
                # let's return object that can't be found
                return self.target_type(
                    and_=frozenset([constants.NEVER_FIND_THIS]),
                    or_=frozenset(sets['or_']),
                    not_=frozenset(sets['not_']),
                    include_realms=frozenset(sets['include_realms']),
                    exclude_realms=frozenset(sets['exclude_realms']),
                    include_themes=frozenset(sets['include_themes']),
                    exclude_themes=frozenset(sets['exclude_themes']),
                    flags=frozenset(sets['flags']),
                )

            self.update_sets(operator, word, sets)

        return self.target_type(
            and_=frozenset(sets['and_']),
            or_=frozenset(sets['or_']),
            not_=frozenset(sets['not_']),
            include_realms=frozenset(sets['include_realms']),
            exclude_realms=frozenset(sets['exclude_realms']),
            include_themes=frozenset(sets['include_themes']),
            exclude_themes=frozenset(sets['exclude_themes']),
            flags=frozenset(sets['flags'])
        )
