import datetime
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from typing import Annotated
from app.config import settings


if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}


engine_nullpool = create_async_engine(DATABASE_URL,
                                      **DATABASE_PARAMS)


async_session_maker = sessionmaker(engine_nullpool,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]
str_not_null = Annotated[str, mapped_column(nullable=False)]
str_null = Annotated[str, mapped_column(nullable=True)]
created_at = Annotated[datetime.date, mapped_column(server_default=text("TIMEZONE('utc', now())"))]