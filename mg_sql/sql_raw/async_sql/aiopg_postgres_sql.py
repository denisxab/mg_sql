"""
"""

from typing import Any, Callable

from .async_base_sql import AsyncBaseCommand
from .async_serializer import Efetch

try:
    # https://aiopg.readthedocs.io/en/stable/core.html
    # pip install aiopg
    from aiopg import connect
    from psycopg2 import OperationalError
except ModuleNotFoundError:
    pass


class Config(AsyncBaseCommand):

    def __init__(self,
                 user: str,
                 password: str,
                 database: str | None = None,
                 port: int = 5432,
                 host: str = "localhost"):
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({
            "port": port,
        })
        if database:
            self.SETTINGS_DB["dbname"] = database
        # self.SETTINGS_DB = ' '.join([f"{_k}={_v}" for _k, _v in self.SETTINGS_DB.items()])

    async def read_command(self, _connection,
                           execute: str,
                           params: tuple | dict | list = (),
                           tdata: Callable = Efetch.all, ) -> Any:
        async with _connection.cursor() as _cur:
            await _cur.execute(execute, params)
            return await tdata(_cur)

    async def transaction_read_command(self, _connection,
                                       execute: str,
                                       params: tuple | dict | list = ()) -> Any:
        pass

    async def mutable_command(self, _connection,
                              execute: str,
                              params: tuple | dict | list = (),
                              ):
        async with _connection.cursor() as _cur:
            await _cur.execute(execute, params)
        return _cur.statusmessage

    async def transaction_mutable_command(self, _connection,
                                          execute: str,
                                          params: tuple | dict | list = ()):
        pass

    @property
    def ERROR(self):
        return OperationalError

    @property
    def ConnectCallback(self):
        return connect
