"""

"""

from .async_base_sql import AsyncBaseCommand

try:
    # https://magicstack.github.io/asyncpg/current/installation.html
    # pip install asyncpg
    from asyncpg import create_pool
    from psycopg2 import OperationalError
except ModuleNotFoundError:
    pass


class Config(AsyncBaseCommand):

    def __init__(self, user: str,
                 password: str,
                 database: str | None = None, port: int = 5432,
                 host: str = "localhost"):
        super().__init__(user, password, host)
        self.SETTINGS_DB.update({"port": port, })
        if database:
            self.SETTINGS_DB["database"] = database

    # self.SETTINGS_DB = ' '.join([f"{_k}={_v}" for _k, _v in self.SETTINGS_DB.items()])

    async def read_command(self, _connection,
                           execute: str,
                           params: tuple | dict | list = (),
                           ) -> list[object]:
        return await _connection.fetch(execute, *params)

    async def transaction_read_command(self, _connection,
                                       execute: str,
                                       params: tuple | dict | list = (),
                                       ) -> list[object]:
        async with _connection.transaction():
            return await _connection.fetch(execute, *params)

    async def mutable_command(self, _connection,
                              execute: str,
                              params: tuple | dict | list = (), ):
        await _connection.execute(execute, *params)

    async def transaction_mutable_command(self, _connection,
                                          execute: str,
                                          params: tuple | dict | list = ()):
        async with _connection.transaction():
            return await _connection.execute(execute)

    async def test(self, execute) -> list[object]:
        """
        https://magicstack.github.io/asyncpg/current/api/index.html

        - fetch(query, *args, timeout=None) → list[source]
          Запустите запрос и верните результаты в виде списка Record.

        - fetchrow(query, *args, timeout=None)[source]
           Запустите запрос и верните первую строку.

        - fetchval(query, *args, column=0, timeout=None)[source]
            Запустите запрос и верните значение в первой строке.

        - execute(query: str, *args, timeout: Optional[float] = None) → str[source]
            Выполните команду (или команды) SQL.
        """

        async with self.ConnectCallback(**self.SETTINGS_DB) as pool:
            # Take a connection from the pool.
            async with pool.acquire() as connection:
                # Open a transaction.
                # async with connection.transaction():
                # Run the query passing the request argument.
                # result = await connection.execute(execute)
                return await connection.fetch(execute)

    @property
    def ConnectCallback(self):
        return create_pool

    @property
    def ERROR(self):
        return OperationalError
