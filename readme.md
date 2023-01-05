# Подготовка

Для работы с БД я создал библиотеку на основе `SqlAlchemy`.

Главно, что нужно сделать для работы с этой библиотекой, это заранее вызвать конструктор класса `SQL`, который создаст
подключение к СУБД

```python
SQL(SqlUrlConnect.СУБД(user='', password='', host='', name_db=''))
```

- `SqlUrlConnect` - Класс с шаблонами формирования `url` для подключения к СУБД

# Использование

## Использование в асинхронной Функции/Методе

```python
import asyncio
from mg_sql.sql_async import SqlUrlConnect
from mg_sql.sql_async.base import SQL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection, AsyncEngine

@SQL.get_session_decor
async def ReadDB(_session: AsyncSession):
    res = await SQL.read_execute_raw_sql(_session, raw_sql=""" SQL ЗАПРОС = :ключ """, params={'ключ':Значение})

asyncio.run(ReadDB())
```

- `raw_sql=''` - SQL запрос
- `params:dict[str,Any]` - Параметры в шаблонные

## Создание таблиц

```python
import asyncio
from mg_sql.sql_async.base import SQL
from mg_sql.sql_async.model_logic import RawSqlModel

class ИмяТаблицы(RawSqlModel):
    """Пользователи"""
    table_name = 'ИмяТаблицы'

    @classmethod
    def create_table(cls) -> str:
        return """
CREATE TABLE ИмяТаблицы (
 id INTEGER,
 user_id INTEGER,
);
CREATE UNIQUE INDEX ix_users_vk_user_id ON users_vk (user_id);
    """

asyncio.run(SQL.create_models(
    [ИмяТаблицы]
))
```

<!-- ## Использование в FastApi

```python
@router.api_route("/Путь", methods=["POST"])
async def ИмяМаршрутизатора(request: Request, session: AsyncSession = Depends(SQL.get_session)):
    res = await SQL.read_execute_raw_sql(session, raw_sql='', params={})
```

- `raw_sql=''` - SQL запрос
- `params:dict[str,Any]` - Параметры в шаблонные
 -->
