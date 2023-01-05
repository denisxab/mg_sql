from collections import namedtuple
from typing import Any, Union

from sqlalchemy import text
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from logsmal import logger
import re

from .helpful import SqlUrlConnect
from .model_logic import RawSqlModel

class SQL:
    """
    Класс для работы с СУБД
    """
    engine: AsyncEngine = None
    async_session: Any = None
    Base: DeclarativeMeta = None

    def __init__(self, url: Union[SqlUrlConnect, str]):
        self._connect(url=url)

    @staticmethod
    def _connect(url: Union[SqlUrlConnect, str]):
        """Подключение к БД"""
        #: Настройки для подключения к БД
        SQL.engine = create_async_engine(url)
        #: Для Сессий
        SQL.async_session = sessionmaker(SQL.engine, class_=AsyncSession, expire_on_commit=False)
        #: Для ORM моделей
        SQL.Base = declarative_base()

    @classmethod
    def get_session_decor(cls, fun):
        """
        @get_session_dec
        async def NameFun(..., session: AsyncSession):
            await session.execute(text('''sql'''))
            # await session.commit()
        """

        async def wrapper(*arg, **kwargs):
            async with cls.async_session() as session:
                res = await fun(*arg, **kwargs, _session=session)
            return res

        return wrapper

    @classmethod
    async def get_session(cls) -> AsyncSession:
        # Получить сессию
        # Получить сессию await get_session().__anext__()
        async with cls.async_session() as session:
            yield session

    @classmethod
    async def get_session_transaction(cls) -> AsyncSession:
        # Получить сессию в транзакции
        # Получить сессию await get_session_transaction().__anext__()
        async with cls.async_session() as session:
            async with session.begin():
                yield session

    @classmethod
    async def write_execute_raw_sql(cls, session: AsyncSession, raw_sql: str,
                                    params: dict[str, Union[str, int, bool, float]] = None) -> int:
        """
        Выполнить SQL запрос на запись, и вернуть результат запроса

        :param session: Сессия
        :param raw_sql: Sql запрос
        :param params: Параметры в sql запрос
        :return:  Выполнено успешных запроса
        """
        cursor = await session.execute(text(raw_sql), params=params)
        await session.commit()
        return cursor.rowcount

    @classmethod
    async def read_execute_raw_sql(cls
        , session: AsyncSession
        , raw_sql: str
        ,params: dict[str, Union[str, int, bool, float]] = None) -> list[dict[str, Any]]:
        """
        Выполнить SQL запрос на чтение, и вернуть результат запроса

        :param session: Сессия
        :param raw_sql: Sql запрос
        :param params: Параметры в sql запрос
        :return: Список ответов list[Row]
        """
        cursor = await session.execute(text(raw_sql), params=params)
        return cls.dictfetchall(cursor)

    @classmethod
    async def execute_raw_sql(cls, raw_sql: str):
        """
        Выполнить сырой SQL запрос

        .. code-block:: python

            import asyncio

            schema = '''
            CREATE TABLE IF NOT EXISTS subscribe
            (
                id      serial PRIMARY KEY,
                user_id bigint unique,
                user_name VARCHAR (255)
            );
            '''

            if __name__ == '__main__':
                asyncio.run(execute_raw_sql(schema))
        """

        async with cls.engine.begin() as conn:
            await conn.execute(text(raw_sql))
            await conn.commit()

    @classmethod
    async def create_tabel(cls):
        """Создать все таблицы"""
        async with cls.engine.begin() as conn:
            conn: AsyncConnection
            await conn.run_sync(cls.Base.metadata.create_all)

    @classmethod
    async def drop_tabel(cls):
        """Удалить все таблицы"""
        async with cls.engine.begin() as conn:
            conn: AsyncConnection
            await conn.run_sync(cls.Base.metadata.drop_all)

    @staticmethod
    def dictfetchall(cursor: CursorResult) -> list[dict[str, Any]]:
        """
        Вернуть ответ в виде словаря

        {"ИмяСтолбца":"Значение"}
        """
        columns = [col[0] for col in cursor.cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def namedtuplefetchall(cursor: CursorResult) -> list[namedtuple]:
        """
        Вернуть ответ в виде именованного картежа

        NamedTuple(ИмяСтолбца=Значение)
        """
        nt_result = namedtuple('_', [col[0] for col in cursor.cursor.description])
        return [nt_result(*row) for row in cursor.fetchall()]


    @staticmethod
    async def create_models(_models:list[RawSqlModel]):
        """
        Создать таблицы в БД, которые указаны в `init_models`
        """
        #  Создать таблицы который указаны через использование BaseMode из
        #  библиотеки SqlAlchemy
        # if len(SQL.Base.metadata.tables) > 0:
        #     async with SQL.engine.begin() as conn:
        #         await conn.run_sync(SQL.Base.metadata.create_all)
        #     logger.info(f"Таблицы созданы {list(SQL.Base.metadata.tables.keys())}")
        # Создать таблицы которые указаны через наследование `RawSqlModel`
        if _models:
            for _table in _models:
                c= _table.create_table()
                for x in c.split(';'):
                    if re.search('\w',x):
                        await SQL.execute_raw_sql(x)
                try:
                    if _table.init_data():
                        await SQL.execute_raw_sql(_table.init_data())
                except DatabaseError as e:
                    logger.warning(f"Ошибка инициализации данных:{e}", ['init_data'])
                logger.info(f"Таблица создана {_table}", ['init_models'])

    @staticmethod
    async def delete_models(_models:list[RawSqlModel]):
        """
        Удалить таблицы из БД, которые подключены к проекту
        """
        if input("Вы действительно хотите удалить все таблицы ? Для подтверждения введите `YES`") == "YES":
            # # Удаляем таблицы модели которых созданы через `BaseMode` из библиотеки SqlAlchemy
            # if len(SQL.Base.metadata.tables) > 0:
            #     async with SQL.engine.begin() as conn:
            #         await conn.run_sync(SQL.Base.metadata.drop_all())
                    # logger.info(f"Таблицы удалены {list(SQL.Base.metadata.tables.keys())}", 'delete_models')
            # Удаляем таблицы которые указаны через наследование `RawSqlModel`
            if _models:
                for _table in _models:
                    _table: RawSqlModel
                    await SQL.execute_raw_sql(_table.drop_table())
                    logger.info(f"Таблица удалена {_table}", 'delete_models')
        else:
            logger.info("Таблицы НЕ удалены")
