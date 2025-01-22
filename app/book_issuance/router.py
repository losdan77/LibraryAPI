import logging
from datetime import date
from fastapi import APIRouter, Depends
from app.exception import MaxCountBookException, ReturnDateException, NoBookReturnException, PermissionDenied
from app.user.models import User
from app.user.dependecies import get_current_user
from app.book_issuance.schemas import SIssuanceBook
from app.book_issuance.dao import BookIssuanceDAO


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix='/book_issuance',
    tags=['Выдача книг']
)


@router.post('/add_book_issuance')
async def add_book_issuance(issuance_data: SIssuanceBook, current_user: User = Depends(get_current_user)):
    '''Выдача книги авторизованному пользователю по ее id, доступно всем пользователям'''

    if current_user['book_count'] >= 5:
        raise MaxCountBookException
    
    today_date = date.today()

    if issuance_data.return_date < today_date:
        raise ReturnDateException
    
    book_issuance = await BookIssuanceDAO.book_issued(id_book = issuance_data.id_book,
                                                      id_user = current_user['id'],
                                                      issuance_date=today_date,
                                                      return_date=issuance_data.return_date,)
    
    logger.info("Успешно добавлена выдача книги ID %d пользователю ID %d", issuance_data.id_book, current_user['id'])
    return book_issuance


@router.post('/return_book')
async def return_book(id_book: int, current_user: User = Depends(get_current_user)):
    '''Возвращение книги авторизованным пользователем по ее id, доступно всем пользователям'''

    exsisting_book = await BookIssuanceDAO.check_exsisting_book(id_book=id_book, id_user=current_user['id'])
    if not exsisting_book:
        raise NoBookReturnException
    
    returned_book = await BookIssuanceDAO.return_book_by_id_book(id_book=id_book, id_user=current_user['id'])

    logger.info("Книга ID %d успешно возвращена пользователем ID %d", id_book, current_user['id'])
    return returned_book


@router.get('/get_my_book')
async def get_my_book(current_user: User = Depends(get_current_user)):
    '''Просмотр авторизованным пользователем, какие книги находятся у него
    на руках, доступно всем пользователям'''

    my_book = await BookIssuanceDAO.find_all(id_user = current_user['id'],
                                             is_return = False)
    return my_book


@router.get('/get_reader_book_issuance_by_id')
async def get_reader_book_issuance_by_id(id_user: int, current_user: User = Depends(get_current_user)):
    '''Просмотр какие книги на руках у пользователя по его id, доступно только администратору'''

    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    reader_book = await BookIssuanceDAO.find_all(id_user = id_user,
                                                 is_return = False)
    return reader_book


@router.get('/get_all_book_issuance')
async def get_all_book_issuance(current_user: User = Depends(get_current_user)):
    '''Просмотр всех книг находящихся на выдаче у пользователей, доступно только администратору'''

    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    all_book = await BookIssuanceDAO.find_all(is_return = False)
    return all_book