## SqlLiteQrm

```python
sq = SqlLiteQrm('data_base.db')
```

---

- `.name_db` = Получить имя БД

---

- `.header_table[]` = Получить заголовок таблиц из БД

---
> Пример

```python
test_header = {"id": PrimaryKey(int),
               "name": toTypeSql(str),
               "old": NotNullDefault(int, 5),
               "salary": NotNull(float)}
sq.CreateTable('name_table', test_header)
assert sq.header_table['name_table'] == {'id': 'INTEGER PRIMARY KEY',
                                         'name': 'TEXT',
                                         'old': 'INTEGER NOT NULL DEFAULT 5',
                                         'salary': 'REAL NOT NULL'}
```

---

- `ListTables()` = Получить имена всех таблиц в БД

---

- `HeadTable(NameTable, width_table: int = 10)` = Выводи в консоль данные о таблицы из БД. `NameTable` имя таблицы,
  `width_table` ширина столбцов.

> Пример

```python
sq.CreateTable('name_table', {"id": toTypeSql(int), "name": toTypeSql(str), "old": toTypeSql(int)})
print(sq.HeadTable('name_table', 15))
```

---

- `GetTable(NameTable: str, LIMIT: Tuple[int, int] = None, FlagPrint: int = 0)` = Получить данные из таблицы в
  БД. `LIMIT(до, шаг)`, `FlagPrint` Указывает печатать ли результат в консоль

> Пример

```python
test_header = {"id": PrimaryKey(int),
               "name": toTypeSql(str),
               "old": NotNullDefault(int, 5),
               "salary": NotNull(float)}
sq.CreateTable('name_table', test_header)
assert sq.header_table['name_table'],
{'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'old': 'INTEGER NOT NULL DEFAULT 5',
 'salary': 'REAL NOT NULL'})
sq.ExecuteTable('name_table', {"id": 1, "name": "Anton", "old": 30, "salary": 3000.11})
sq.ExecuteTable('name_table', {"id": 2, "name": "Katy", "old": 22, "salary": 3200.23})
assert sq.GetTable('name_table') == [(1, 'Anton', 30, 3000.11), (2, 'Katy', 22, 3200.23)]
```  

--- 

- `GetColumn(NameTable: str, name_columns: str, LIMIT: Tuple[int, int] = None)` = Получить данные из столбца таблицы в
  БД

> Пример

```python
sq.CreateTable(self.name_table,
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict(self.name_table,
                        [{"name": "Denis", "old": 21},
                         {"name": "Katy", "old": 21, "sex": 1},
                         {"name": "Svetha", "old": 24}]
                        )
assert self.sq.GetColumn(self.name_table, "name") == ['Denis', 'Katy', 'Svetha']
assert self.sq.GetColumn(self.name_table, "old") == [21, 21, 24]
assert self.sq.GetColumn(self.name_table, "old", LIMIT=(2, 0)) == [21, 21]
```

---

- `DeleteTable(NameTable: Union[str, List[str]])` = Удалить одну таблицу или несколько таблиц

---

- `DeleteLineTable(NameTable: str, sqlWHERE: str = "")` = Удалить строки по условию `WHERE`

> Пример

```python
sq.CreateTable('name_table',
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict('name_table', [{"name": "Denis", "old": 21},
                                       {"name": "Katy", "old": 221, "sex": 1},
                                       {"name": "Mush", "old": 321, "sex": 21},
                                       {"name": "Patio", "old": 231, "sex": 21},
                                       {"name": "Pvetha", "old": 24}])
sq.DeleteLineTable('name_table', "old > 25")
assert sq.GetTable('name_table') == [(1, 'Denis', 21, '_'), (5, 'Pvetha', 24, '_')]
```

---

- `CreateTable(NameTable: str, columns: Union[str, Dict])` = Создать таблицу с заголовками столбцов `columns`.
  Используйте вспомогательные функции из `sqlmodules` для удобного создание sql запросов

> Пример

```python
# Должны содержать уникальные значения
PrimaryKey = lambda TypeColumn: definition(TypeColumn) + " PRIMARY KEY"
# Всегда должно быть заполнено
NotNull = lambda TypeColumn: definition(TypeColumn) + " NOT NULL"
# Все столбцы будут по умолчанию заполнены указанными значениями
NotNullDefault = lambda TypeColumn, default: definition(TypeColumn) + f" NOT NULL DEFAULT {default}"
# Значение по умолчанию
Default = lambda TypeColumn, default: definition(TypeColumn) + " DEFAULT {0}".format(default)
# Авто заполнение строки. подходит для id
PrimaryKeyAutoincrement = lambda TypeColumn: definition(TypeColumn) + " PRIMARY KEY AUTOINCREMENT"
# Конвертация  типа данных python в SQLLite
toTypeSql = lambda TypeColumn: definition(TypeColumn)
```

- `ExecuteTable(NameTable: str, data: Union[str, int, float, List[Union[str, bytes, int, float]], Tuple, Dict[str, Union[str, bytes, int, float]]] = None, sqlRequest: str = "", *, CheckBLOB: bool = False)`
  = Добавить запись в таблицу из БД
  `sqlRequest` вы можете добавить данные из sql запрос.`CheckBLOB` если вы записываете бинарные данные в таблицу
  используйте этот флаг.

> Пример

```python
sq.CreateTable('name_table',
               {"id": toTypeSql(int),
                "old": toTypeSql(int)
                })
test_table: str = 'test_table'
sq.CreateTable(test_table,
               {"old": toTypeSql(int)})

sq.ExecuteManyTable('name_table',
                    [[11, 24],
                     [22, 31],
                     [2312, 312],
                     [231, 68],
                     [344, 187]])

resSQL = Select('name_table', "id").Where("id < 30").Request

sq.ExecuteTable(test_table, sqlRequest=resSQL)

assert sq.GetTable(test_table) == [(11,), (22,)]
```

> Пример `CheckBLOB`

```python
test_header = {"str": toTypeSql(str), "int": toTypeSql(int), "float": toTypeSql(float),
               "bytes": toTypeSql(bytes)}
sq.CreateTable('name_table', test_header)
test_data = ("text", 123, 122.32, b"1011")
sq.ExecuteTable('name_table', test_data, CheckBLOB=True)
assert sq.GetTable('name_table')[0] == test_data
```            

- `ExecuteManyTable(NameTable: str, data: List[Union[List[Union[str, bytes, Binary, int, float]], Tuple]], head_data: Union[List[str], Tuple] = None, *, CheckBLOB: bool = False)`
  = Добавить несколько записей в таблицу в формате List. `head_data` указывать когда длинна входных данных меньше чем
  количество столбцов в таблице

> Пример

```python
sq.CreateTable('name_table', {
    'car_id': PrimaryKeyAutoincrement(int),
    "model": toTypeSql(str),
    "price": toTypeSql(int)
})

car = [
    ("Audi", 432),
    ("Maer", 424),
    ("Skoda", 122)
]
sq.ExecuteManyTable('name_table', car, head_data=("model", "price"))
assert sq.GetTable('name_table') == [(1, 'Audi', 432), (2, 'Maer', 424), (3, 'Skoda', 122)]
```

- `ExecuteManyTableDict(NameTable: str, data: List[Dict])` = Добавить несколько записей в таблицу в формате Dict

> Пример

```python
sq.CreateTable('name_table',
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict('name_table',
                        [{"name": "Denis", "old": 21},
                         {"name": "Katy", "old": 21, "sex": 1},
                         {"name": "Svetha", "old": 24}]
                        )
assert sq.Search(Select('name_table', "name").Where("old == 21")) == [('Denis',), ('Katy',)]
```

- `UpdateColumne(NameTable: str, name_column: Union[str, List[str]], new_data: Union[str, bytes, int, float, List[Union[str, bytes, int, float]]], sqlWHERE: str = "")`
  = Обновить данные в столбцах таблицы по условию `sqlWHERE`

> Пример

```python
sq.CreateTable('name_table',
               {"id": PrimaryKeyAutoincrement(int), "name": toTypeSql(str), "old": toTypeSql(int),
                "sex": NotNullDefault(str, "_")})
sq.ExecuteManyTableDict('name_table', [{"name": "Denis", "old": 21},
                                       {"name": "Katy", "old": 221, "sex": 1},
                                       {"name": "Mush", "old": 321, "sex": 21},
                                       {"name": "Patio", "old": 231, "sex": 21},
                                       {"name": "Svetha", "old": 24}])

sq.UpdateColumne('name_table', 'old', 99)
assert sq.GetTable('name_table') == [(1, 'Denis', 99, '_'),
                                     (2, 'Katy', 99, '1'),
                                     (3, 'Mush', 99, '21'),
                                     (4, 'Patio', 99, '21'),
                                     (5, 'Svetha', 99, '_')]
```

- `Search` = Поиск данных в таблице
- `SaveDbToFile` = Сохранить БД в отдельный
- `ReadFileToDb`
- `DeleteDb` 





