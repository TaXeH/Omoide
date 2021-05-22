# -*- coding: utf-8 -*-

"""Fully processed user search request.
"""
from itertools import chain
from typing import FrozenSet, NamedTuple, Dict, List

from omoide.core import constants


class Query(NamedTuple):
    """Fully processed user search request.
    """
    and_: FrozenSet[str]
    or_: FrozenSet[str]
    not_: FrozenSet[str]
    include_realms: FrozenSet[str]
    exclude_realms: FrozenSet[str]
    include_themes: FrozenSet[str]
    exclude_themes: FrozenSet[str]
    flags: FrozenSet[str]

    def __str__(self) -> str:
        """Reconstruct query from known arguments."""
        keywords = chain.from_iterable(self.as_keywords().values())
        return ' '.join(keywords)

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'<{type(self).__name__}, n={self.total_items()}>'

    def __bool__(self) -> bool:
        """Return True if query has actual words to search."""
        return bool(self.and_ or self.or_)

    def total_items(self) -> int:
        """Return total amount of registered items."""
        return sum(map(len, [self.and_, self.or_, self.not_,
                             self.include_realms, self.exclude_realms,
                             self.include_themes, self.exclude_themes,
                             self.flags]))

    def as_keywords(self) -> Dict[str, List[str]]:
        """Return sorted collection of internal keywords."""

        def _str(attribute: str, collection: frozenset) -> List[str]:
            """Shorthand construction."""
            value = getattr(constants.Operators, attribute).value
            return [f'{value} {x}' for x in sorted(collection)]

        return {
            'and_': _str('KW_AND', self.and_),
            'or_': _str('KW_OR', self.or_),
            'not_': _str('KW_NOT', self.not_),
            'include_realms': _str('KW_INCLUDE_R', self.include_realms),
            'exclude_realms': _str('KW_EXCLUDE_R', self.exclude_realms),
            'include_themes': _str('KW_INCLUDE_T', self.include_themes),
            'exclude_themes': _str('KW_EXCLUDE_T', self.exclude_themes),
            'flags': _str('KW_FLAG', self.flags),
        }

    def as_dict(self) -> Dict[str, List[str]]:
        """Return representation of the query as a dict."""
        return {
            'and_': sorted(self.and_),
            'or_': sorted(self.or_),
            'not_': sorted(self.not_),
            'include_realms': sorted(self.include_realms),
            'exclude_realms': sorted(self.exclude_realms),
            'include_themes': sorted(self.include_themes),
            'exclude_themes': sorted(self.exclude_themes),
            'flags': sorted(self.flags),
        }
