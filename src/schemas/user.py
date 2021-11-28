from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

    @validator('name')
    def phone_validator(cls, v):
        if v is None:
            raise ValueError("Имя пользователя не может быть пустым!")
        return v


class UserIn(UserBase):
    password: str
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Пароли не совпадают")
        return v


class UserOut(UserBase):
    id: int
    pass


class UserOutWithToken(BaseModel):
    user: UserBase
    access_token: str

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    access_token: str
