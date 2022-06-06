from typing import get_args, List, Set, TypeVar, Union

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.preconditions import check_argument
from hspylib.core.tools.text_tools import quote

T = TypeVar('T')
FILTER_VALUE = TypeVar('FILTER_VALUE', int, str, bool, float)


class FilterConditions(Enumeration):
    """TODO"""

    # @formatter:off
    LESS_THEN                   =      '<', Union[int, float]
    LESS_THEN_OR_EQUALS_TO      =     '<=', Union[int, float]
    GREATER_THEN                =      '>', Union[int, float]
    GREATER_THEN_OR_EQUALS_TO   =     '>=', Union[int, float]
    EQUALS_TO                   =     '==', Union[str, int, bool, float]
    DIFFERENT_FROM              =     '!=', Union[str, int, bool, float]
    CONTAINS                    =     'in', Union[str]
    DOES_NOT_CONTAIN            = 'not in', Union[str]
    IS                          =     '==', Union[bool]
    IS_NOT                      =     '!=', Union[bool]
    # @formatter:on

    def __str__(self):
        return self.name.lower().replace('_', ' ')

    def __repr__(self):
        return str(self)

    def matches(self, param_value: FILTER_VALUE, value: FILTER_VALUE) -> bool:
        """TODO"""
        return self._has_type(value) \
               and (
                   eval(f'{quote(value)} {self.value[0]} {quote(param_value)}')
                   if self.name in ['CONTAINS', 'DOES_NOT_CONTAIN']
                   else eval(f'{param_value} {self.value[0]} {value}')
               )

    def _has_type(self, value: FILTER_VALUE) -> bool:
        """TODO"""
        try:
            return isinstance(value, self.value[1])
        except TypeError:
            return isinstance(value, get_args(self.value[1]))

class ElementFilter:

    def __init__(
        self, name: str,
        el_name: str,
        condition: 'FilterConditions',
        el_value: FILTER_VALUE):
        self.name = name
        self.el_name = el_name
        self.condition = condition
        self.el_value = el_value

    def __str__(self):
        return f'{quote(self.el_name)} {self.condition} {quote(self.el_value)}'

    def __repr__(self):
        return str(self)

    def matches(self, element: T) -> bool:
        """TODO"""
        try:
            entry = element if isinstance(element, dict) else element.__dict__
            return self.el_name in entry \
                   and self.condition.matches(entry[self.el_name], self.el_value)
        except (NameError, TypeError, AttributeError):
                return False


class CollectionFilter:
    """TODO"""

    def __init__(self):
        self._filters: Set[ElementFilter] = set()

    def __str__(self):
        return ' '.join([f"{'AND ' if i > 0 else ''}{str(f)}" for i, f in enumerate(self._filters)])

    def __repr__(self):
        return str(self)

    def apply_filter(
        self, name: str,
        el_name: str,
        condition: 'FilterConditions',
        el_value: Union[int, str, bool, float]) -> None:
        """TODO"""

        check_argument(not any(f.name == name for f in self._filters),
                       f'Filter {name} already exists!')

        self._filters.add(ElementFilter(name, el_name, condition, el_value))

    def clear(self) -> None:
        """TODO"""
        self._filters.clear()

    def discard(self, name: str):
        """TODO"""
        element = next((e for e in self._filters if e.name == name), None)
        self._filters.discard(element)

    def filter(self, data: List[T]) -> List[T]:
        """TODO"""
        filtered: List[T] = []
        for element in data:
            if all(f.matches(element) for f in self._filters):
                filtered.append(element)
        return filtered

    def filter_reverse(self, data: List[T]) -> List[T]:
        """TODO"""
        filtered: List[T] = []
        for element in data:
            if not any(f.matches(element) for f in self._filters):
                filtered.append(element)
        return filtered


if __name__ == '__main__':
    arr = [
        {'id': 0, 'name': 'hugo', 'age': 43, 'score': 9.8, 'active': True},
        {'id': 1, 'name': 'joao', 'age': 22, 'score': 2.5, 'active': True},
        {'id': 2, 'name': 'juca', 'age': 15, 'score': 4.0, 'active': True},
        {'id': 3, 'name': 'kako', 'age': 67, 'score': 3.9, 'active': True},
        {'id': 4, 'name': 'lucas', 'age': 33, 'score': 5.0, 'active': True},
        {'id': 5, 'name': 'gabits', 'age': 1, 'score': 7.8, 'active': False},
        {'id': 6, 'name': 'claudia', 'age': 34, 'score': 6.1, 'active': True},
        {'id': 7, 'name': 'be', 'age': 10, 'score': 10.0, 'active': False},
    ]
    f = CollectionFilter()
    f.apply_filter('f1', 'score', FilterConditions.GREATER_THEN_OR_EQUALS_TO, 5.0)
    f.apply_filter('f2', 'active', FilterConditions.IS, True)
    f.apply_filter('f3', 'name', FilterConditions.CONTAINS, 'u')
    f.apply_filter('f4', 'age', FilterConditions.LESS_THEN_OR_EQUALS_TO, 40)
    print(f'Filters: {f}')
    print('\n'.join([str(e) for e in f.filter(arr)]))
