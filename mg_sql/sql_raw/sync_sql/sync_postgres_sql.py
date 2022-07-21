"""

"""

from typing import Any, Callable

from .sync_base_sql import SyncBaseSql
from .sync_serializer import Efetch

try:
    from psycopg2 import OperationalError, connect
except ModuleNotFoundError:
    pass


class Config(SyncBaseSql):
    @property
    def CONNECT(self):
        return connect

    @property
    def ERROR(self):
        return OperationalError

    def __init__(self, user: str,
                 password: str,
                 database: str | None = None,
                 port: int = 5432,
                 host: str = "localhost"):
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({
            "port": port,
        })
        if database:
            self.SETTINGS_DB["database"] = database

    def read_command(self, _connection,
                     execute: str,
                     params: tuple | dict | list = (),
                     tdata: Callable = Efetch.all,
                     *args,
                     **kwargs) -> Any:
        """
        Декоратор для выполнения чтения из БД
        """
        with _connection.cursor() as cursor:
            cursor.execute(execute, params)
            return tdata(cursor)

    def mutable_command(self, _connection,
                        execute: str,
                        params: tuple | dict | list = (),
                        autocommit: bool = False,
                        *args,
                        **kwargs):
        """
        Декоратор для выполнения изменяемой SQL команды
        """
        # Автоматический коммит
        _connection.autocommit = autocommit
        with _connection.cursor() as cursor:
            cursor.execute(execute, params)
            _connection.commit()
        return cursor.statusmessage
