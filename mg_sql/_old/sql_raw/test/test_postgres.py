from pprint import pprint

import sql_raw.async_sql.aiopg_postgres_sql
import sql_raw.async_sql.async_serializer
import sql_raw.async_sql.asyncpg_postgres_sql
import sql_raw.sync_sql.sync_postgres_sql
import sql_raw.sync_sql.sync_serializer
from .base_dataset_test import NAME_DB, HOST, Refresh_TABLE, NAME_TABEL


def refresh_db():
    """
     Если `FATAL: Peer authentication failed for user "postgres"`

     1. Установить или сменить пароль для пользователя `postgres`
         `sudo passwd postgres;`

     2. Изменить способ подключения е БД
         `sudo micro /etc/postgresql/12/main/pg_hba.conf`
         "
         local   all             postgres                                password
         "
     3. Перезагрузить БД
         `sudo systemctl restart  postgresql`
     """
    # Подключаемся к СУБД
    db = sql_raw.sync_sql.sync_postgres_sql.Config(user="postgres", password="root", host=HOST)
    # Удаляем БД
    print(db.wsql(f"DROP DATABASE IF EXISTS {NAME_DB};", autocommit=True))
    # Создаем БД
    db.wsql(f"CREATE DATABASE {NAME_DB};", autocommit=True)

class Test_Sync:

    def setup(self):
        refresh_db()
        # Подключаемся к БД
        self.db = sql_raw.sync_sql.sync_postgres_sql.Config(user="postgres", password="root", database=NAME_DB,
                                                            host=HOST)
        # Создаем таблицу
        self.db.wsql(Refresh_TABLE)

    def test_write(self):
        self.db.wsql(f"""
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
        assert self.db.Rsql(
            f"SELECT * FROM {NAME_TABEL}") == "[(1, 'dcurrington0@umn.edu', '955,00 ₽'),\n (2, 'rhartland1@blog.com', '430,00 ₽'),\n (3, 'zkinton2@so-net.ne.jp', '817,00 ₽'),\n (4, 'btuison6@themeforest.net', '281,00 ₽'),\n (5, 'gczajka4@tinypic.com', '610,00 ₽'),\n (6, 'btuison6@themeforest.net', '281,00 ₽'),\n (7, 'btuison6@themeforest.net', '281,00 ₽'),\n (8, 'aclancy7@tmall.com', '884,00 ₽'),\n (9, 'zkinton2@so-net.ne.jp', '817,00 ₽'),\n (10, 'ndelaperrelle9@smh.com.au', '523,00 ₽')]"

        assert self.db.rsql(f"SELECT * FROM {NAME_TABEL}") == [
            (1, 'dcurrington0@umn.edu', '955,00 ₽'),
            (2, 'rhartland1@blog.com', '430,00 ₽'),
            (3, 'zkinton2@so-net.ne.jp', '817,00 ₽'),
            (4, 'btuison6@themeforest.net', '281,00 ₽'),
            (5, 'gczajka4@tinypic.com', '610,00 ₽'),
            (6, 'btuison6@themeforest.net', '281,00 ₽'),
            (7, 'btuison6@themeforest.net', '281,00 ₽'),
            (8, 'aclancy7@tmall.com', '884,00 ₽'),
            (9, 'zkinton2@so-net.ne.jp', '817,00 ₽'),
            (10, 'ndelaperrelle9@smh.com.au', '523,00 ₽')]

        assert self.db.rsql(f"SELECT * FROM {NAME_TABEL}", tdata=sql_raw.sync_sql.sync_serializer.Efetch.dict_) == [
            {'id': 1, 'email': 'dcurrington0@umn.edu', 'buy': '955,00 ₽'},
            {'id': 2, 'email': 'rhartland1@blog.com', 'buy': '430,00 ₽'},
            {'id': 3, 'email': 'zkinton2@so-net.ne.jp', 'buy': '817,00 ₽'},
            {'id': 4, 'email': 'btuison6@themeforest.net', 'buy': '281,00 ₽'},
            {'id': 5, 'email': 'gczajka4@tinypic.com', 'buy': '610,00 ₽'},
            {'id': 6, 'email': 'btuison6@themeforest.net', 'buy': '281,00 ₽'},
            {'id': 7, 'email': 'btuison6@themeforest.net', 'buy': '281,00 ₽'},
            {'id': 8, 'email': 'aclancy7@tmall.com', 'buy': '884,00 ₽'},
            {'id': 9, 'email': 'zkinton2@so-net.ne.jp', 'buy': '817,00 ₽'},
            {'id': 10, 'email': 'ndelaperrelle9@smh.com.au', 'buy': '523,00 ₽'}]

        assert self.db.Rsql(f"SELECT * FROM {NAME_TABEL}",
                            tdata=sql_raw.sync_sql.sync_serializer.Efetch.namedtuple) == "[_(id=1, email='dcurrington0@umn.edu', buy='955,00 ₽'),\n _(id=2, email='rhartland1@blog.com', buy='430,00 ₽'),\n _(id=3, email='zkinton2@so-net.ne.jp', buy='817,00 ₽'),\n _(id=4, email='btuison6@themeforest.net', buy='281,00 ₽'),\n _(id=5, email='gczajka4@tinypic.com', buy='610,00 ₽'),\n _(id=6, email='btuison6@themeforest.net', buy='281,00 ₽'),\n _(id=7, email='btuison6@themeforest.net', buy='281,00 ₽'),\n _(id=8, email='aclancy7@tmall.com', buy='884,00 ₽'),\n _(id=9, email='zkinton2@so-net.ne.jp', buy='817,00 ₽'),\n _(id=10, email='ndelaperrelle9@smh.com.au', buy='523,00 ₽')]"

        assert self.db.rsql(f"SELECT * FROM {NAME_TABEL}",
                            tdata=sql_raw.sync_sql.sync_serializer.Efetch.one) == (
                   1, 'dcurrington0@umn.edu', '955,00 ₽')


class Test_Async:

    def setup(self):
        refresh_db()
        # Подключаемся к БД
        self.db = sql_raw.async_sql.asyncpg_postgres_sql.Config(user="postgres", password="root", database=NAME_DB)
        # Создаем таблицу
        self.db.appendTask(self.db.wsql(Refresh_TABLE))
        self.db.executeTasks()

    def test_write(self):
        self.db.appendTask(self.db.wsql(f"""
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
         """, isTransaction=True))
        self.db.executeTasks()
        self.db.extendTask(
            [self.db.Rsql(f"SELECT * FROM {NAME_TABEL};"), self.db.Rsql(f"SELECT * FROM {NAME_TABEL};", )])
        assert self.db.executeTasks() == [
            "[<Record id=1 email='dcurrington0@umn.edu' buy='955,00 ₽'>,\n <Record id=2 email='rhartland1@blog.com' buy='430,00 ₽'>,\n <Record id=3 email='zkinton2@so-net.ne.jp' buy='817,00 ₽'>,\n <Record id=4 email='btuison6@themeforest.net' buy='281,00 ₽'>,\n <Record id=5 email='gczajka4@tinypic.com' buy='610,00 ₽'>,\n <Record id=6 email='btuison6@themeforest.net' buy='281,00 ₽'>,\n <Record id=7 email='btuison6@themeforest.net' buy='281,00 ₽'>,\n <Record id=8 email='aclancy7@tmall.com' buy='884,00 ₽'>,\n <Record id=9 email='zkinton2@so-net.ne.jp' buy='817,00 ₽'>,\n <Record id=10 email='ndelaperrelle9@smh.com.au' buy='523,00 ₽'>]",
            "[<Record id=1 email='dcurrington0@umn.edu' buy='955,00 ₽'>,\n <Record id=2 email='rhartland1@blog.com' buy='430,00 ₽'>,\n <Record id=3 email='zkinton2@so-net.ne.jp' buy='817,00 ₽'>,\n <Record id=4 email='btuison6@themeforest.net' buy='281,00 ₽'>,\n <Record id=5 email='gczajka4@tinypic.com' buy='610,00 ₽'>,\n <Record id=6 email='btuison6@themeforest.net' buy='281,00 ₽'>,\n <Record id=7 email='btuison6@themeforest.net' buy='281,00 ₽'>,\n <Record id=8 email='aclancy7@tmall.com' buy='884,00 ₽'>,\n <Record id=9 email='zkinton2@so-net.ne.jp' buy='817,00 ₽'>,\n <Record id=10 email='ndelaperrelle9@smh.com.au' buy='523,00 ₽'>]"]


def test_test():
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
    ###
    db = sql_raw.async_sql.async_postgres_sql.Config(user="postgres", password="root", database=NAME_DB, host=HOST)
    db.extendTask([db.test(f"SELECT * FROM {NAME_TABEL};"),  # db.test(f"SELECT * FROM {NAME_TABEL};"),
                   # db.test(f"SELECT * FROM {NAME_TABEL};"),
                   # db.rsql(f"SELECT * FROM {NAME_TABEL};"),
                   # db.rsql(f"SELECT id FROM {NAME_TABEL};"),
                   # db.Rsql(f"SELECT * FROM {NAME_TABEL};"),
                   # db.Rsql(f"SELECT * FROM {NAME_TABEL};"),
                   ])
    pprint(db.executeTasks())
