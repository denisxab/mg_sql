from abc import abstractclassmethod, abstractmethod
from typing import TypedDict, Union, Optional

class RawSqlModel:
    """
    Интерфейс для создания моделей в SQL, с сырыми sql запросами для создания модели
    """
    all_tables: dict[str, object] = {}

    @property
    @abstractmethod
    def table_name(self):
        ...

    @abstractclassmethod
    def create_table(cls) -> str:
        """
        SQL код для создания таблицы
        """
        ...

    @abstractclassmethod
    def init_data(cls) -> str:
        """Инициализировать данные в БД"""
        ...

    @staticmethod
    def drop_table() -> str:
        """
        SQL код для удаления таблицы
        """
        ...


class SqlTypeReturn(TypedDict):
    """
    Тип для результата

    Пример

    ..code-block::python

        from users.model import User
        from vetcin_pack_fastapi.database_pack.model_logic import SqlTypeReturn

        class UserLogic(User):

            @classmethod
            def login(cls, login: str, password: str) -> SqlTypeReturn:
                return dict(
                    raw_sql='''
            select
                id
            from users
            where login = ':login'
            and hash_password = ':hash_password'
                ''',
                    params={"login": login, "password": password}
                )
    """
    raw_sql: str
    params: Optional[dict[str, Union[str, int, float, bool]]]

