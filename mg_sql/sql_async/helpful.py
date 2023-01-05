from hashlib import sha512
from random import randint
from typing import Any, TypedDict


class ExtendColumn(TypedDict):
    # Тип
    type: Any
    # Тип для html формы
    html_input_type: str
    # Описание
    description: str
    # Внешние связи
    foreign_keys: Any
    # Разрешить Null
    nullable: bool
    # Первичный ключ
    primary_key: Any
    # Уникальность
    unique: bool


class SqlUrlConnect:
    """
    Шаблон URL для подключения к СУБД
    """

    @staticmethod
    def sqllite(path_db: str):
        return f'sqlite+aiosqlite:///{str(path_db)}'

    @staticmethod
    def postgresql(user: str, password: str, host: str, name_db: str, port: int = 5432):
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name_db}"


# Захешировать пароль
def hashPassword(password: str) -> str:
    return sha512(password.encode('utf-8')).hexdigest()


# Случайный хеш
def hashRandom() -> str:
    return hashPassword(str(randint(0, 100_000_000)))
