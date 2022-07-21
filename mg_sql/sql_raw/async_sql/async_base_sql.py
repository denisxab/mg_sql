from abc import abstractmethod, ABCMeta
from asyncio import run, gather
from collections import deque
from pprint import pformat
from typing import Any, Coroutine, Callable

from logsmal import logger

from .async_serializer import BaseTasks
from ..base_sql import BaseSql


class AsyncBaseSql(BaseSql, BaseTasks, metaclass=ABCMeta):
    """
    Базовый асинхронны класс
    """

    def __init__(self,
                 user: str,
                 password: str,
                 host: str = "localhost"):
        # Создаем настройки
        BaseSql.__init__(self, user, password, host)
        # Создаем список с задач
        BaseTasks.__init__(self)
        self.Poll: Callable | object | None = None
        self.FuncConnectDb: Callable | object | None = None

    # BASE CONNECT
    async def executeTasks(self):
        """Запустить выполнения задач"""
        res = await self._run(self.tasks)
        self.tasks.clear()
        return res

    async def _run(self, tasks: deque[Coroutine]):
        self.FuncConnectDb = self.connect_db
        """Выполнить список задач"""
        return await gather(*tasks)

    async def connect_db(self, fun: Callable, *args, **kwargs) -> Any:
        """
        Так как у нас всегда включен `autocommit` мы
        можем использовать контекстный менеджер `with`
        """
        try:
            async with self.ConnectCallback(**self.SETTINGS_DB) as connection:
                return await fun(connection, *args, **kwargs)
        except self.ERROR as e:
            logger.error(e)
            raise e

    # POOL

    def executeTasksPool(self):
        """Запустить выполнения задач"""
        res = run(self._run_pool(self.tasks))
        self.tasks.clear()
        return res

    async def _run_pool(self, tasks: deque[Coroutine]):
        """Выполнить список задач"""
        self.FuncConnectDb = self.connect_pool
        # Создаем пул соединений
        async with self.ConnectCallback(**self.SETTINGS_DB) as pool:
            # Сохраняем пул в экземпляре
            self.Poll = pool
            # Запускаем запросы
            return await gather(*tasks)

    async def connect_pool(self, fun: Callable, *args, **kwargs):
        try:
            async with self.Poll.acquire() as connection:
                return await fun(connection, *args, **kwargs)
        except self.ERROR as e:
            logger.error(e)
            raise e

    # Abstract
    @property
    @abstractmethod
    def ERROR(self):
        ...

    @property
    @abstractmethod
    def ConnectCallback(self):
        ...


class AsyncBaseCommand(AsyncBaseSql, metaclass=ABCMeta):
    """
    from sql_raw.async_sql.async_postgres_sql import Config
    from sql_raw.async_sql.async_serializer import Efetch

    # Создать конфигурацию
    db = Config(user="postgres", password="root", database="fast_api")

    # Добавить список задач
    db.extendTask([
        db.rsql("SELECT * FROM пользователь;", tdata=Efetch.dict_),
        db.rsql("SELECT id FROM пользователь;"),
        db.rsql("SELECT * FROM пользователь;"),
    ])

    # Добавить одну задачу
    db.appendTask(db.rsql("SELECT * FROM пользователь;"))

    # Выполнить задачи
    pprint(db.executeTasks())
    """

    def __init__(self,
                 user: str,
                 password: str,
                 host: str = "localhost"):
        AsyncBaseSql.__init__(self, user, password, host)

    async def rsql(self, execute: str,
                   params: tuple | dict | list = ()) -> str:
        """
        Чтение из БД
        """
        res = await self.FuncConnectDb(self.read_command,
                                       execute=execute,
                                       params=params)
        return res

    async def rsql_transaction(self, execute: str,
                               params: tuple | dict | list = ()) -> str:
        """
        Чтение из БД транзакция
        """
        return await self.FuncConnectDb(self.transaction_read_command,
                                        execute=execute,
                                        params=params)

    async def wsql(self, execute: str,
                   params: tuple | dict | list = (),
                   ) -> tuple[str, tuple | dict | list]:
        """
        Внесение изменений в БД
        """
        return await self.FuncConnectDb(self.mutable_command,
                                        execute=execute
                                        , params=params)

    async def wsql_transaction(self, execute: str,
                               params: tuple | dict | list = (),
                               ) -> tuple[str, tuple | dict | list]:
        """
        Внесение изменений в БД
        """
        return await self.FuncConnectDb(self.transaction_mutable_command,
                                        execute=execute,
                                        params=params)

    # Утилиты
    async def Rsql(self, execute: str,
                   params: tuple | dict | list = (),
                   isTransaction: bool = False) -> str:
        """
        Чтение из БД с красивым выводом в консоль
        """
        return await self.pprint_deco(self.rsql,
                                      execute,
                                      params,
                                      isTransaction)

    @staticmethod
    async def pprint_deco(fun: Callable,
                          execute: str,
                          params: tuple | dict | list = (),
                          isTransaction: bool = False
                          ) -> str:
        """
        Декоратор для красивого вывода результата функции в консоль
        """
        return pformat(await fun(execute, params, isTransaction))

    # Abstractmethod
    @abstractmethod
    async def read_command(self, _connection,
                           execute: str,
                           params: tuple | dict | list = (), ):
        """
        Метод для выполнения чтения из БД
        """
        return NotImplemented()

    @abstractmethod
    async def mutable_command(self, _connection,
                              execute: str,
                              params: tuple | dict | list = (), ):
        """
        Метод для выполнения записи в БД
        """
        return NotImplemented()

    @abstractmethod
    async def transaction_mutable_command(self, _connection,
                                          execute: str,
                                          params: tuple | dict | list = (),
                                          ):
        return NotImplemented()

    @abstractmethod
    async def transaction_read_command(self, _connection,
                                       execute: str,
                                       params: tuple | dict | list = (),
                                       ) -> Any:
        return NotImplemented()
