from __future__ import annotations
from typing import Any, Callable
from .special_cases import Zero, Null, Empty
from .query import Limit, Offset


class QueryBuilder:
    ZERO = Zero()
    NULL = Null()
    EMTPY = Empty()
    _SPECIAL_CASES = (Zero(), Null(), Empty())

    def __init__(self):
        self.limit = Limit()
        self.offset = Offset()
        self._filters = []
        self._orders = []
        self._params = []

    def add(self, value: Any, condition: str) -> QueryBuilder:
        if value:
            val = value.value if value in self._SPECIAL_CASES else value
            self._filters.append(condition)
            self._params.append(val)

        return self

    def in_(self, value: Any, condition: str) -> QueryBuilder:
        if value:
            values = value.split(",")
            xs = tuple([v.strip() for v in values])
            self._filters.append(condition)
            self._params.append(xs)

        return self

    def between(self, ranges: list, keyword: str) -> QueryBuilder:
        down, up = ranges

        if down and up:
            self._filters.append(f"{keyword} BETWEEN %s AND %s")
            self._params.append(down)
            self._params.append(up)
        elif down:
            self._filters.append(f"{keyword} >= %s")
            self._params.append(down)
        elif up:
            self._filters.append(f"{keyword} <= %s")
            self._params.append(up)

        return self

    def like(self, value: Any, condition: str, transform: Callable) -> QueryBuilder:
        if value:
            self._filters.append(condition)
            self._params.append(transform(value))

        return self

    def add_order_by(self, value: Any, condition: str) -> QueryBuilder:
        if value:
            self._orders.append(condition.format(value))

        return self

    @property
    def where(self) -> str:
        if len(self._filters) == 0:
            return "WHERE 1 = 1"

        conditions = " AND ".join(self._filters)
        return f"WHERE {conditions}"

    @property
    def order_by(self) -> str:
        if len(self._orders) == 0:
            return ""

        orders = ", ".join(self._orders)
        return f"ORDER BY {orders}"

    @property
    def params(self):
        return self._params
