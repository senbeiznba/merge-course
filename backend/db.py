from collections.abc import Iterator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from config import settings

# Шаблоны имен для ограничений (constraints), чтобы они совпадали с PostgreSQL
NAMING_CONVENTION = {
    "ix": "%(table_name)s_%(column_0_N_name)s_idx",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

engine = create_engine(settings.database_url, echo=settings.sql_echo)
SessionLocal = sessionmaker(engine)

def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session