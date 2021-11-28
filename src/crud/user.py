from fastapi_sqlalchemy import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from src.exceptions import UniqueDataException
from src.models.models import UserModel
from src.schemas.user import UserIn
from src.utils.utils import hash_password


def create_user(user: UserIn) -> UserModel:
    db_user = UserModel(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )
    try:
        db.session.add(db_user)
        db.session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            db.session.rollback()
            raise UniqueDataException()
    return db_user


def get_user_by_email(email: str) -> UserModel:
    return db.session.query(UserModel).filter(UserModel.email == email).first()
