from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.exception import NoAuthorization, UserTokenException
from app.config import settings
from app.user.dao import UserDAO


async def get_token(request: Request):
    try:
        token = request.cookies['access_token']
    except:
        raise NoAuthorization
    return token

    
async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_WORD, settings.HASH_ALGORITHM
        )
    except JWTError:
        raise UserTokenException

    expire: str = payload['exp']
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise UserTokenException

    user_id: str = payload['sub']
    if not user_id:
        raise UserTokenException
    
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserTokenException
    
    user_dict = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role,
        'book_count': user.book_count,
        'created_at': user.created_at,
    }

    return user_dict