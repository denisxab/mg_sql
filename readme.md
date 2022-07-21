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
@SQL.get_session_decor
async def ReadDB(self, Lik: bool, session: AsyncSession):
    res = await SQL.read_execute_raw_sql(session, raw_sql='', params={})
```

- `raw_sql=''` - SQL запрос
- `params:dict[str,Any]` - Параметры в шаблонные

## Использование в FastApi

```python
@router.api_route("/Путь", methods=["POST"])
async def ИмяМаршрутизатора(request: Request, session: AsyncSession = Depends(SQL.get_session)):
    res = await SQL.read_execute_raw_sql(session, raw_sql='', params={})
```

- `raw_sql=''` - SQL запрос
- `params:dict[str,Any]` - Параметры в шаблонные

