from hashlib import sha512
import json
from random import randint
from typing import Any, TypedDict
from re import sub, Match


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

    # @staticmethod
    # def firebird(user: str, password: str, host: str, name_db: str, port: int = 3050):
    #     # Не получилось внедрить Firebird 11.02.2023. Используй https://github.com/denisxab/fbutils
    #     return f"firebird+fdb://{user}:{password}@{host}:{port}/{name_db}"


def textSql(text: str, params: dict[str, str]):
    """ 
    Собрать SQL запрос, с экранированием параметров 

    :::::::::::::::::::Гайд:::::::::::::::

    :name%s - Строка, вставиться как = 'Значение'
    :name%i - Цела цифра, вставиться как = 111
    :name%f - Дробная цифра, вставиться как = 11.11
    :name%j - JSON строка, вставиться как = '{"name":123}'


    text="select * from user where id=:name%i"          --- params={"name":1}
    text="select * from user where user_name=:name%s"   --- params={"name":"xable"}

    """
    def _self(m: Match) -> str:
        md = m.groupdict()
        _res = None
        match md['t']:
            case "s":
                # Экранирование одинарных кавычек
                _res = "'{0}'".format(
                    str(params[md['key']]).replace("'", "''"))
            case "j":
                _res = "'{0}'".format(json.dumps(params[md['key']]))
            case "i":
                _res = int(params[md['key']])
            case "f":
                _res = float(params[md['key']])
        return str(_res)
    return sub(r":(?P<key>[\w\d]+)%(?P<t>[isfj])", _self, text)


# Захешировать пароль
def hashPassword(password: str) -> str:
    return sha512(password.encode('utf-8')).hexdigest()


# Случайный хеш
def hashRandom() -> str:
    return hashPassword(str(randint(0, 100_000_000)))
