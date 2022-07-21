from collections import namedtuple
from enum import Enum
from typing import Callable, Any


def dictfetchall(cursor) -> list[dict[str, Any]]:
    """
    Вернуть в виде словаря
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor) -> list[namedtuple]:
    """
    Вернуть в виде именовано го картежа
    """
    desc = cursor.description
    nt_result = namedtuple('_', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class Efetch(Enum):
    dict_: Callable[[Any], list[dict[str, Any]]] = dictfetchall
    namedtuple: Callable[[Any], list[namedtuple]] = namedtuplefetchall
    one: Callable[[Any], Any] = lambda _cursor: _cursor.fetchone()
    all: Callable[[Any], Any] = lambda _cursor: _cursor.fetchall()
