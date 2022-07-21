from abc import abstractmethod
from pprint import pformat
from typing import Any, Callable

from logsmal import logger

from .sync_serializer import Efetch
from ..base_sql import BaseSql


class SyncBaseSql(BaseSql):

    def connect_db(self, fun: Callable, *args, **kwargs) -> Any:
        """
        Так как у нас может быть подключение с транзакцией и без, мы не можем использовать
        контекстный менеджер `with`, так как он обязательно создает транзакцию.
        Поэтому мы сами обрабатываем исключения и закрываем соединение с БД.
        """
        connection = self.CONNECT(**self.SETTINGS_DB)
        try:
            return fun(connection, *args, **kwargs)
        except self.ERROR as e:
            logger.error(e)
            raise e
        finally:
            connection.close()

    def rsql(self, execute: str, params: tuple | dict | list = (), tdata: Callable = Efetch.all,
             ) -> tuple[str, tuple | dict | list]:
        """
        Чтение из БД
        """
        return self.connect_db(self.read_command, execute=execute, params=params, tdata=tdata)

    def Rsql(self, execute: str, params: tuple | dict | list = (), tdata: Callable = Efetch.all) -> str:
        """
        Чтение из БД с красивым выводом в консоль
        """
        return self.pprint_deco(self.rsql(execute, params, tdata))

    def wsql(self, execute: str,
             params: tuple | dict | list = (),
             autocommit: bool = False) -> tuple[str, tuple | dict | list]:
        """
        Внесение изменений в БД

        @param execute: `SQL` команда
        @param params: Вставить данные в `SQL` команду
        @param autocommit: Если вы используете `autocommit` то передувайте одну `SQL` команду. Установите `True`
        если вы выполняете команды связанные с СУБД.
        """
        return self.connect_db(self.mutable_command, execute=execute, params=params, autocommit=autocommit)

    @staticmethod
    def pprint_deco(d: Any) -> str:
        """
        Декоратор для красивого вывода результата функции в консоль
        """
        return pformat(d)

    @abstractmethod
    def read_command(self, _connection,
                     execute: str,
                     params: tuple | dict | list = (),
                     tdata: Callable = Efetch.all,
                     *args,
                     **kwargs):
        """
        Декоратор для выполнения чтения из БД
        """
        return NotImplemented()

    @abstractmethod
    def mutable_command(self, _connection,
                        execute: str,
                        params: tuple | dict | list = (),
                        *args,
                        **kwargs):
        """
        Декоратор для выполнения изменяемой SQL команды
        """
        return NotImplemented()

    @property
    @abstractmethod
    def CONNECT(self):
        pass

    @property
    @abstractmethod
    def ERROR(self):
        ...
