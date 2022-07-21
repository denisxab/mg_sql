from abc import ABCMeta
from collections import deque
from collections import namedtuple
from enum import Enum
from typing import Any, Coroutine, Callable


class BaseTasks(metaclass=ABCMeta):
    """
    Базовый класс для списка асинхронных задач.
    Используются как примесь к асинхронному классу `AsyncBaseSql`
    """

    def __init__(self):
        self.tasks: deque[Coroutine] = deque()

    def appendTask(self, coroutine: Coroutine):
        """Добавить здание в список"""
        self.tasks.append(coroutine)

    def extendTask(self, coroutine: list[Coroutine] | deque[Coroutine]):
        """Расширить список задач другим списком список"""
        self.tasks.extend(coroutine)


async def dictfetchall(cursor) -> list[dict[str, Any]]:
    """
    Вернуть в виде словаря
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in await cursor.fetchall()
    ]


async def namedtuplefetchall(cursor) -> list[namedtuple]:
    """
    Вернуть в виде именовано го картежа
    """
    desc = cursor.description
    nt_result = namedtuple('_', [col[0] for col in desc])
    return [nt_result(*row) for row in await cursor.fetchall()]


async def _fetchone(cursor):
    return await cursor.fetchone()


async def _fetchall(cursor):
    return await cursor.fetchall()


class Efetch(Enum):
    dict_: Callable[[Any], list[dict[str, Any]]] = dictfetchall
    namedtuple: Callable[[Any], list[namedtuple]] = namedtuplefetchall
    one: Callable[[Any], Any] = _fetchone
    all: Callable[[Any], Any] = _fetchall
