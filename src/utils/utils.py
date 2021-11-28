import datetime
import os

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv(".env")
SECRET_KEY = os.getenv("SECRET_KEY")


def hash_password(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def verify_password(raw_password: str, hash: str) -> bool:
    return pwd_context.verify(raw_password, hash)


def generate_jwt_auth(email: str) -> str:
    return jwt.encode(
        {
            "sub": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        SECRET_KEY,
        algorithm="HS256",
    )