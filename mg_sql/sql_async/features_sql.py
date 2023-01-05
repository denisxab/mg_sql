try:
    from sqlalchemy import text, insert
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.decl_api import DeclarativeMeta
except ImportError:
    pass


class FeaturesSql:
    """
    Особенности SQL
    """

    """
    Префикс для игнорирования исключений
    при вставке значений, например игнорировать вставку
    не уникального значения в столбце

    :Пример:

    sql_ = await _session.execute(
    insert(
            UsersVk, 
            prefixes=[SqlLite.prefixes_ignore_insert]
        ),
        arr_user
    )
    """
    prefixes_ignore_insert = ''


class SqlLite(FeaturesSql):
    prefixes_ignore_insert = 'OR IGNORE'


class MySql(FeaturesSql):
    prefixes_ignore_insert = 'IGNORE'


class SqlScript:

    @classmethod
    async def set_row_skip_unique(
            cls,
            models,
            params,
            dbms: FeaturesSql,
            _session: AsyncSession
    ):
        """
        Вставить запись игнорирую уникальность
        """
        await _session.execute(insert(models, prefixes=[dbms.prefixes_ignore_insert]), params)
        await _session.commit()

    @classmethod
    async def set_row_if_not_unique(cls, sql_get, sql_set, _session: AsyncSession):
        """
        Вставить запись если она не уникальная

        :return: Запись
        """
        # Проверяем наличие записи в БД
        response = await _session.execute(sql_get)
        sql_obj = response.first()
        if not sql_obj:
            # Если записи нет, то добавляем ей в БД
            _session.add(sql_set)
            await _session.commit()
            return sql_set
        else:
            # Если он есть, то возвращаем полученный объект
            return sql_obj[0]
