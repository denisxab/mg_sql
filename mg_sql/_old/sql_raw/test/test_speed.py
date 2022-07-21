import time

import sql_raw.async_sql.aiopg_postgres_sql
import sql_raw.async_sql.async_serializer
import sql_raw.async_sql.asyncpg_postgres_sql
import sql_raw.sync_sql.sync_postgres_sql
import sql_raw.sync_sql.sync_serializer
from .base_dataset_test import NAME_DB, HOST
from .test_postgres import NAME_TABEL, Test_Sync


def test_speed_async(SQL_COMMAND: str, LEN: int):
    start = time.process_time()
    db = sql_raw.async_sql.asyncpg_postgres_sql.Config(user="postgres", password="root", database=NAME_DB, host=HOST)
    db.extendTask([
        db.rsql_transaction(SQL_COMMAND) for _ in range(LEN)
    ])
    res = db.executeTasksPool()
    end = time.process_time()
    print([len(x) for x in res])
    print("asYncpg", end - start)


def test_speed_t_async(SQL_COMMAND: str, LEN: int):
    start = time.process_time()
    db = sql_raw.async_sql.aiopg_postgres_sql.Config(user="postgres", password="root", database=NAME_DB, host=HOST)
    db.extendTask([
        db.rsql(SQL_COMMAND) for _ in range(LEN)
    ])
    res = db.executeTasks()
    end = time.process_time()
    print([len(x) for x in res])
    print("aiOpg", end - start)


def test_speed_sync(SQL_COMMAND: str, LEN: int):
    start = time.process_time()
    db = sql_raw.sync_sql.sync_postgres_sql.Config(user="postgres", password="root", database=NAME_DB, host=HOST)
    res = [
        db.rsql(SQL_COMMAND) for _ in range(LEN)
    ]
    end = time.process_time()
    print([len(x) for x in res])
    print("SYNC:", end - start)


def test_main_speed():
    Test_Sync().setup()
    db = sql_raw.sync_sql.sync_postgres_sql.Config(user="postgres", password="root", database=NAME_DB, host=HOST)
    db.wsql(f"""
     INSERT INTO {NAME_TABEL} (id, email, buy)
     VALUES (1, 'dcurrington0@umn.edu', 955),
            (2, 'rhartland1@blog.com', 430),
            (3, 'zkinton2@so-net.ne.jp', 817),
            (4, 'btuison6@themeforest.net', 281),
            (5, 'gczajka4@tinypic.com', 610),
            (6, 'btuison6@themeforest.net', 281),
            (7, 'btuison6@themeforest.net', 281),
            (8, 'aclancy7@tmall.com', 884),
            (9, 'zkinton2@so-net.ne.jp', 817),
            (10, 'ndelaperrelle9@smh.com.au', 523);
     """)
    SQL_COMMAND = f"SELECT * FROM {NAME_TABEL}"
    print("START")
    LEN = 100
    test_speed_async(SQL_COMMAND, LEN)
    test_speed_t_async(SQL_COMMAND, LEN)
    test_speed_sync(SQL_COMMAND, LEN)
