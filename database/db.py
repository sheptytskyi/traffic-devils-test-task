import typing as t
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from configuration.config import config


DATABASE_URL = config.database.dsn


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
Base: DeclarativeMeta = declarative_base()
async_session: sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> t.AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
