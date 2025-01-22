from fastapi import APIRouter, Response, Depends
from app.exception import VerifyPasswordException, HasExistingUserException, \
ErrorLoginException, VerifyOldPasswordException, OldAndNewPasswordEqException, PermissionDenied
from app.user.schemas import SUserRegistr, SUserLogin, SUserChangePassword
from app.user.dao import UserDAO
from app.user.models import User
from app.user.auth import get_password_hash, authenticate_user, create_access_token
from app.user.dependecies import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['Пользователи (администраторы и читатели)']
)


@router.post('/registr')
async def registr_user(user_data: SUserRegistr):
    '''Регистрация пользователя, для читателя role=reader, а для администратора role=admin'''

    if user_data.password != user_data.password_verify:
        raise VerifyPasswordException
    
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HasExistingUserException
    
    hashed_password = get_password_hash(user_data.password)

    user = await UserDAO.add(email = user_data.email,
                             hashed_password = hashed_password,
                             name = user_data.name,
                             role = user_data.role,)
    return user
    

@router.post('/login')
async def login_organization(response: Response, user_data: SUserLogin):
    '''Авторизация ползователя, занесение jwt токена в куку'''

    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise ErrorLoginException
    
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_organization(response: Response):
    '''Выход пользователя, удаление куки'''

    response.delete_cookie('access_token')
    return 'done'


@router.post('/me')
async def me_user(current_user: User = Depends(get_current_user)):
    '''Просмотр информации об авторизованном пользователе'''

    return current_user


@router.post('/change_password')
async def change_pasword(user_data: SUserChangePassword, current_user: User = Depends(get_current_user)):
    '''Смена пароля авторизованного пользователя, доступно всем пользователям'''

    verify_old_password = await authenticate_user(current_user['email'], user_data.old_password)
    if not verify_old_password:
        raise VerifyOldPasswordException
    
    if user_data.old_password == user_data.new_password:
        raise OldAndNewPasswordEqException
    
    if user_data.new_password != user_data.verify_new_password:
        raise VerifyPasswordException
    
    new_hashed_password = get_password_hash(user_data.new_password)
    
    updated_user = await UserDAO.update_by_id(id = current_user['id'],
                                              hashed_password = new_hashed_password)
    return updated_user


@router.patch('/change_name')
async def change_name(new_user_name: str, current_user: User = Depends(get_current_user)):
    '''Смена имени авторизованного пользователя, доступно всем пользователям'''

    updated_user = await UserDAO.update_by_id(id = current_user['id'],
                                              name = new_user_name)
    return updated_user


@router.get('/get_all_users')
async def get_all_users(current_user: User = Depends(get_current_user)):
    '''Просмотр списка всех пользователей, доступно только администратору'''
    
    if current_user['role'] != 'admin':
        raise PermissionDenied
    
    users = await UserDAO.find_all()
    return users