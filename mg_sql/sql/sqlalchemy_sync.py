from os import environ

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
except ImportError:
    pass

try:
    engine = create_engine(
        # "postgresql+psycopg2://ИмяПользователя:Пароль@Домен/БД"
        f"postgresql+psycopg2://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@{environ['POSTGRES_IP']}/{environ['POSTGRES_DB']}"
    )
    Session = sessionmaker(bind=engine)
    # Для ORM моделей
    Base = declarative_base()
except Exception as ex:
    print(f"Ошибка: {ex}")

def get_session_decor(fun):
    """
    @get_session_dec
    async def NameFun(..., session: AsyncSession):
        await session.execute(text('''sql'''))
        # await session.commit()
    """

    def wrapper(*arg, **kwargs):
        with Session() as session:
            res = fun(*arg, **kwargs, _session=session)
        return res

    return wrapper


@get_session_decor
def execute_raw_sql(raw_sql: str, _session):
    """
    Выполнить raw SQL
    """
    _session.execute(text(raw_sql))
    _session.commit()
