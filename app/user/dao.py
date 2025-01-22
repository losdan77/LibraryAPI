from sqlalchemy import select, insert, delete, update
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.user.models import User


class UserDAO(BaseDAO):
    model = User


    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(
                        User.id,
                        User.email,
                        User.name,
                        User.role,
                        User.book_count,
                        User.created_at
                    )
            result = await session.execute(query)
            return result.mappings().all() 