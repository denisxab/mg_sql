from abc import ABCMeta
from typing import Any


class BaseSql(metaclass=ABCMeta):
    def __init__(self, user: str, password: str,
                 host: str = "localhost", ):
        self.SETTINGS_DB: dict[str, Any] | str = {"host": host,
                                                  "user": user,
                                                  "password": password}
