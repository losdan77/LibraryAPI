from sqlalchemy import select, insert, update, and_, text
from datetime import date
from app.exception import NoBookInLibraryException
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.book.models import Book 
from app.user.models import User
from app.book_issuance.models import Book_issuance

class BookIssuanceDAO(BaseDAO):
    model = Book_issuance


    @classmethod
    async def book_issued(cls, id_book: int, id_user: int, issuance_date: date, return_date: date):
        async with async_session_maker() as session:
            async with session.begin():
                
                query = select(Book.count_avaliable_copies).where(Book.id==id_book)
                book_avaliable_count = await session.execute(query)
                
                if book_avaliable_count.mappings().one()['count_avaliable_copies'] <= 0:
                    raise NoBookInLibraryException
            
                query = update(Book).where(Book.id==id_book).values(count_avaliable_copies = Book.count_avaliable_copies - 1)
                await session.execute(query)
                
                query = update(User).where(User.id==id_user).values(book_count = User.book_count + 1)
                await session.execute(query)
                
                query = insert(cls.model).returning(cls.model.__table__).values(issuance_date = issuance_date,
                                                                                return_date = return_date,
                                                                                id_book = id_book,
                                                                                id_user = id_user)
                result = await session.execute(query)

                return result.mappings().one()
            

    @classmethod
    async def check_exsisting_book(cls, id_user, id_book):
        async with async_session_maker() as session:
            query = select(Book_issuance.__table__).limit(1).where(and_(Book_issuance.id_user==id_user,
                                                     Book_issuance.id_book==id_book,
                                                     Book_issuance.is_return==False,))
            result = await session.execute(query)
            return result.mappings().one_or_none()
        

    @classmethod
    async def return_book_by_id_book(cls, id_book: int, id_user: int):
        async with async_session_maker() as session:
            async with session.begin():

                query = update(Book).where(Book.id==id_book).values(count_avaliable_copies = Book.count_avaliable_copies + 1)
                await session.execute(query)
                
                query = update(User).where(User.id==id_user).values(book_count = User.book_count - 1)
                await session.execute(query)
                
                query = f"""
                    update book_issuance
                    set is_return = True
                    where id = (select id from book_issuance
                    where id_book = {id_book} and id_user = {id_user} and is_return = false 
                    order by issuance_date asc limit 1) returning *;
                """
                result = await session.execute(text(query))
                return result.mappings().one()