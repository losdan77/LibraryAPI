from sqlalchemy import select
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.author.models import Author


class AuthorDAO(BaseDAO):
    model = Author


    @classmethod
    async def find_all(cls, limit_: int, offset_: int, name: str):
        async with async_session_maker() as session:
            query = select(Author.__table__).limit(limit_).offset(offset_).where(Author.name.like(f'%{name}%'))
            result = await session.execute(query)
            return result.mappings().all()  