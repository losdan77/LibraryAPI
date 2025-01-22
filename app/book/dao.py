from datetime import date
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.book.models import Book 


class BookDAO(BaseDAO):
    model = Book


    @classmethod
    async def find_all(cls, limit_: int, offset_: int, name: str):
        async with async_session_maker() as session:
            query = select(
                            Book
                        ).limit(
                            limit_
                            ).offset(
                                    offset_
                                ).options(
                selectinload(Book.author)
                ).where(Book.name.like(f'%{name}%'))
            result = await session.execute(query)
            return result.mappings().all()  
        
    
    @classmethod
    async def find_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(Book).options(selectinload(Book.author)).filter_by(id=id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    
    @classmethod
    async def add(cls, name: str, description: str, date_pub: date, count_avaliable_copies: int, genre: str, author: list[int]):
        async with async_session_maker() as session:
            async with session.begin():
                query = f"""
                    WITH inserted_book AS (
                        INSERT INTO book (name, description, date_pub, count_avaliable_copies, genre)
                        VALUES ('{name}', '{description}', '{date_pub}', {count_avaliable_copies}, '{genre}')
                        RETURNING id
                    )
                    INSERT INTO book_author (id_book, id_author)
                    SELECT id, unnest(ARRAY{author}) FROM inserted_book;
                """
                await session.execute(text(query))
                