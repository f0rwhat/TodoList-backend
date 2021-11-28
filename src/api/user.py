import datetime
import os
from typing import Union, List

import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from fastapi import APIRouter, Response, Depends
from fastapi_sqlalchemy import db
from jwt import PyJWTError

from src.crud.user import create_user, get_user_by_email
from src.exceptions import UserNotFoundException, WrongDataException, UnauthorizedAccess, JWTExpiredException
from src.schemas.info import ResponseInfo, NotVerifiedScheme
from src.schemas.user import UserBase, UserIn, UserOut, UserOutWithToken, AccessToken
from src.models.models import UserModel
from src.schemas.info import ResponseInfo
from src.utils.utils import verify_password, generate_jwt_auth


load_dotenv(".env")
SECRET_KEY = os.getenv("SECRET_KEY")


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        email: str = payload.get("sub")
        exp_time_stamp = payload.get("exp")

        exp_date = datetime.datetime.fromtimestamp(exp_time_stamp / 1e3)
        now: datetime = datetime.datetime.utcnow()

        if email is None or exp_time_stamp is None:
            raise UnauthorizedAccess()
        if exp_date > now:
            raise JWTExpiredException()
    except PyJWTError:
        raise UnauthorizedAccess()
    user = get_user_by_email(email)
    if user is None:
        raise UnauthorizedAccess()
    return user


@router.post(
    "/user/register",
    response_model=UserOutWithToken,
    responses={200: {"model": UserOutWithToken}, 400: {"model": ResponseInfo}},
)
async def registration_user(user: UserIn):
    db_user = create_user(user)
    encoded = generate_jwt_auth(user.email)
    return {"user": UserBase(name=db_user.name, email=db_user.email), "access_token": encoded, "token_type": "bearer"}


@router.post("/user/login",
             response_model=AccessToken,
             responses={404: {"model": ResponseInfo}}
             )
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    user = get_user_by_email(email)
    if user is None:
        raise UserNotFoundException()
    if not verify_password(form_data.password, user.password):
        raise WrongDataException()
    else:
        access_token = generate_jwt_auth(email)
        return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/user",
    response_model=UserOut,
    responses={401: {"model": ResponseInfo}}
)
def get_user_handler(current_user: UserOut = Depends(get_current_user)):
    return current_user
