from fastapi import APIRouter, Depends
from app.exception import PermissionDenied
from app.user.models import User
from app.user.dependecies import get_current_user
from app.author.schemas import SAddAuthor, SUpdateAuthorBio
from app.author.dao import AuthorDAO


router = APIRouter(
    prefix='/author',
    tags=['Авторы']
)


@router.post('/add_author')
async def add_author(author_data: SAddAuthor, current_user: User = Depends(get_current_user)):
    '''Добавление авторов, доступно только администраторам'''
    
    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    author = await AuthorDAO.add(name = author_data.name,
                                 bio = author_data.bio,
                                 date_b = author_data.date_b)
    return author


@router.get('/get_all_authors')
async def get_all_authors(limit_: int = 5, page: int = 1, name: str = ''):
    '''Просмотр всех авторов, с настроенной пагинацией и фильтрацией по имени автора,
    доступно без авторизации'''
    
    offset_ = (page - 1) * limit_

    authors = await AuthorDAO.find_all(limit_=limit_, offset_=offset_, name=name)
    return authors


@router.get('/get_author_by_id')
async def get_author_by_id(id_author: int):
    '''Вывод автора по его id, доступно без авторизации'''

    author = await AuthorDAO.find_by_id(id = id_author)
    return author


@router.patch('/update_author_bio_by_id')
async def update_author_bio_by_id(author_data: SUpdateAuthorBio, current_user: User = Depends(get_current_user)):
    '''Изменение биографии автора, доступно только админу'''

    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    author = await AuthorDAO.update_by_id(id = author_data.id_author,
                                          bio = author_data.bio)
    return author


@router.delete('/delete_author_by_id')
async def delete_author_by_id(id_author: int, current_user: User = Depends(get_current_user)):
    '''Удаление автора, по его id, доступно только администратору'''
    
    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    await AuthorDAO.delete(id = id_author)
    return 'done'