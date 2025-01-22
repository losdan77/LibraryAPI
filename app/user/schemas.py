from pydantic import BaseModel, EmailStr


class SUserRegistr(BaseModel):
    email: EmailStr
    password: str
    password_verify: str
    name: str
    role: str = 'reader'


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserChangePassword(BaseModel):
    old_password: str
    new_password: str
    verify_new_password: str