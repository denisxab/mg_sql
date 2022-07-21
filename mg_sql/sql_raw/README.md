# Api

- `rsql`(`SQlКоманда, ПараметрыВставки, tdata=`)->`Any` - Получить данные из БД
    - `tdata:Callable=Efetch.all` - Тип возвращаемых данных
        - `Efetch.all` - `cursor.fetchall()`
        - `Efetch.dict` - Тип `dict`
        - `Efetch.namedtuple` - Тип `namedtuple`
        - `Efetch.one` - `cursor.fetchone()`

- `Rsql`(`SQlКоманда,ПараметрыВставки, tdata=`)->`str` - Получить красиво отформатированные данные из БД
    - `tdata:Callable=Efetch.all` - Тип возвращаемых данных
        - `Efetch.all` - `cursor.fetchall()`
        - `Efetch.dict` - Тип `dict`
        - `Efetch.namedtuple` - Тип `namedtuple`
        - `Efetch.one` - `cursor.fetchone()`

- `wsql`(`SQlКоманда,ПараметрыВставки`)->`str` - Записать данные в БД

- `Config`() - Создать объект для взаимодействия с СУБД

# Пример использование

## Синхронный `PostgreSQl`

```bash
pip install psycopg2-binary
```

```python
from mg_file.sql_raw.sync_sql.sync_postgres_sql import Config
from mg_file.sql_raw.sync_sql.sync_serializer import Efetch

NAME_DB = "test_db"
NAME_TABEL = "test_tabel"

db = Config(user="postgres", password="root", database=NAME_DB)
db.wsql(f"""    
CREATE TABLE {NAME_TABEL}
(
    id     serial PRIMARY KEY,
    f_name varchar(255) NOT NULL,
    l_name varchar(255) NOT NULL
);
INSERT INTO пользователь (id, f_name, l_name)
VALUES (1, 'Carola', 'Yandle'),
       (2, 'Risa', 'Follet'),
       (3, 'Cele', 'Caslin'),
       (4, 'Osgood', 'Demead'),
       (5, 'Roldan', 'Malby'),
       (6, 'Reynard', 'Garlee'),
       (7, 'Erna', 'Vigurs'),
       (8, 'Stewart', 'Naismith'),
       (9, 'Poppy', 'Watling'),
       (10, 'Sybila', 'Teliga');
""")
print(db.Rsql(f"SELECT * FROM {NAME_TABEL}", tdata=Efetch.dict_))
```

## Асинхронный `PostgreSQl`

```bash
pip install psycopg2-binary aiopg
```

```python
from mg_file.sql_raw.async_sql.asyncpg_postgres_sql import Config
from mg_file.sql_raw.async_sql.async_serializer import Efetch

NAME_DB = "test_db"
NAME_TABEL = "test_tabel"

db = Config(user="postgres", password="root", database=NAME_DB)
db.appendTask(
    db.wsql(f"""    
    CREATE TABLE {NAME_TABEL}
    (
        id     serial PRIMARY KEY,
        f_name varchar(255) NOT NULL,
        l_name varchar(255) NOT NULL
    );
    INSERT INTO пользователь (id, f_name, l_name)
    VALUES (1, 'Carola', 'Yandle'),
           (2, 'Risa', 'Follet'),
           (3, 'Cele', 'Caslin'),
           (4, 'Osgood', 'Demead'),
           (5, 'Roldan', 'Malby'),
           (6, 'Reynard', 'Garlee'),
           (7, 'Erna', 'Vigurs'),
           (8, 'Stewart', 'Naismith'),
           (9, 'Poppy', 'Watling'),
           (10, 'Sybila', 'Teliga');
    """)
)
db.executeTasks()
db.appendTask(db.Rsql(f"SELECT * FROM {NAME_TABEL}", tdata=Efetch.namedtuple))
print(db.executeTasks())
```