from fastapi import APIRouter, Depends
from app.exception import PermissionDenied
from app.user.models import User
from app.user.dependecies import get_current_user
from app.book.schemas import SAddBook, SUpdateCountAvaliableCopies
from app.book.dao import BookDAO


router = APIRouter(
    prefix='/book',
    tags=['Книги']
)


@router.post('/add_book')
async def add_book(book_data: SAddBook, current_user: User = Depends(get_current_user)):
    '''Добавление книги, доступно только администратору'''

    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    await BookDAO.add(name = book_data.name,
                      description = book_data.description,
                      date_pub = book_data.date_pub,
                      count_avaliable_copies = book_data.count_avaliable_copies,
                      genre = book_data.genre,
                      author = book_data.id_author)
    return 'done'


@router.get('/get_all_books')
async def get_all_books(limit_: int = 5, page: int = 1, name: str = ''):
    '''Вывод всех книг, с настроенной пагинацией и фильтром по названию,
    доступно без авторизации'''

    offset_ = (page - 1) * limit_

    books = await BookDAO.find_all(limit_=limit_, offset_=offset_, name=name)
    return books


@router.get('/get_book_by_id')
async def get_book_by_id(id_book: int):
    '''Вывод книги по ее id, доступно без авторизации'''

    book = await BookDAO.find_by_id(id = id_book)
    return book


@router.patch('/update_count_avaliable_copies_by_id')
async def update_count_avaliable_copies_by_Id(book_data: SUpdateCountAvaliableCopies, 
                                              current_user: User = Depends(get_current_user)):
    '''Обновление остатков книг в библиотеке, доступно только администратору'''

    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    book = await BookDAO.update_by_id(id = book_data.id_book,
                                      count_avaliable_copies = book_data.count_avaliable_copies)
    return book


@router.delete('/delete_book_by_id')
async def delete_book_by_id(id_book: int, current_user: User = Depends(get_current_user)):
    '''Удаление книги по ее id, доступно только администратору'''
    
    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    await BookDAO.delete(id = id_book)
    return 'done'


