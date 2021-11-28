import os
from typing import Union, List

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi_sqlalchemy import db
from pydantic import EmailStr
from starlette import status

from src.api.user import get_current_user
from src.crud.projects import get_projects_of_user, create_new_project, delete_project, update_project_info, \
    get_project, add_user_to_project, get_users_of_project, delete_user_from_project, check_user_is_maintainer
from src.exceptions import JWTExpiredException, GenericException
from src.models.models import ProjectModel
from src.schemas.info import ResponseInfo, NotVerifiedScheme
from src.schemas.project import Project, ProjectOut
from src.schemas.user import AccessToken, UserBase, UserOut

router = APIRouter()


@router.get(
    "/projects/{project_id}",
    response_model=ProjectOut,
    responses={401: {"model": ResponseInfo}}
)
def get_project_handler(project_id: int, current_user: UserOut = Depends(get_current_user)):
    return get_project(project_id, current_user.id)


@router.get(
    "/projects",
    response_model=List[ProjectOut],
    responses={401: {"model": ResponseInfo}}
)
def get_projects_handler(current_user: UserOut = Depends(get_current_user)):
    return get_projects_of_user(current_user.id)


@router.post(
    "/projects",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def create_project_handler(project: Project, current_user: UserOut = Depends(get_current_user)):
    return create_new_project(project, current_user.id)


@router.delete(
    "/projects/{project_id}",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def delete_project_handler(project_id: int, current_user: UserOut = Depends(get_current_user)):
    return delete_project(project_id, current_user.id)


@router.put(
    "/projects/{project_id}",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def update_project_handler(project_id: int, project: Project, current_user: UserOut = Depends(get_current_user)):
    return update_project_info(project_id, project, current_user.id)


@router.get(
    "/projects/{project_id}/users",
    response_model=List[UserBase],
    responses={401: {"model": ResponseInfo}}
)
def get_users_of_project_handler(project_id: int, current_user: UserOut = Depends(get_current_user)):
    return get_users_of_project(project_id, current_user.id)


@router.post(
    "/projects/{project_id}/users",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def add_user_to_project_handler(project_id: int, email: EmailStr, current_user: UserOut = Depends(get_current_user)):
    return add_user_to_project(project_id, email, current_user.id)


@router.delete(
    "/projects/{project_id}/users",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def delete_user_from_project_handler(project_id: int, email: EmailStr, current_user: UserOut = Depends(get_current_user)):
    return delete_user_from_project(project_id, email, current_user.id)


@router.get(
    "/projects/{project_id}/check_maintain_permission",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def check_maintain_permission_handler(project_id: int, email: EmailStr, current_user: UserOut = Depends(get_current_user)):
    return check_user_is_maintainer(project_id, current_user.id)
