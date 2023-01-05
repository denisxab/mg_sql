from abc import abstractstaticmethod
from hashlib import sha512


class UserNameDontExistsError(Exception):
    def __str__(self):
        return "Пользователь с таким `user name` не существует"


def hashPassword(password: str) -> str:
    """
    Захеширвоать пароль
    """
    return sha512(password.encode('utf-8')).hexdigest()


class BaseSchema:
    """
    Базовая SQL модель
    """

    @abstractstaticmethod
    def create_tabel():
        """
        Создать таблицу в БД
        """
        ...
