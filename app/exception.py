from fastapi import status, HTTPException


HasExistingUserException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Данный пользовать уже существует',
)

VerifyPasswordException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пароли не совпадают',
)

ErrorLoginException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный email или пароль',
)

NoAuthorization = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Пользователь неавторизован',
)

UserTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Ошибка токена доступа',
)

PermissionDenied =HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Недостаточно прав',
)

VerifyOldPasswordException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Старый пароль не совпадает',
)

OldAndNewPasswordEqException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Новый пароль должен отличаться от старого',
)

MaxCountBookException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Запрещено держать у себя более 5 книг',
)

ReturnDateException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Дата возвращения книги долдна быть такой же или позднее даты выдачи',
)

NoBookReturnException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='У вас нет данной книги',
)

NoBookInLibraryException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Данной книги не осталось в библиотеке',
)