"""

"""

from typing import Callable

from .sync_base_sql import SyncBaseSql
from .sync_serializer import Efetch

try:
    from sync_mysql.connector import connect, Error
except ModuleNotFoundError:
    pass


class Config(SyncBaseSql):

    @property
    def CONNECT(self):
        return connect

    @property
    def ERROR(self):
        return Error

    def __init__(self, user: str, password: str, dbname: str | None = None,
                 port: int = 3306,
                 host: str = "localhost"):
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({
            "port": port,
            "dbname": dbname,
        })

    def mutable_command(self, _connection,
                        execute: str,
                        params: tuple | dict | list = (),
                        autocommit: bool = False,
                        *args,
                        **kwargs):
        """
        Декоратор для выполнения изменяемой SQL команды
        """
        with _connection.cursor() as cursor:
            cursor.execute(execute, params, multi=kwargs["multi"])
            _connection.commit()
        return cursor.statement

    def read_command(self, _connection,
                     execute: str,
                     params: tuple | dict | list = (),
                     tdata: Callable = Efetch.all,
                     *args,
                     **kwargs):
        """
        Декоратор для выполнения чтения из БД
        """
        with _connection.cursor() as cursor:
            cursor.execute(execute, params, multi=kwargs["multi"])
            return tdata(cursor)
