from typing import Union, List
from starlette import status
from fastapi import APIRouter, Response, Depends
from fastapi_sqlalchemy import db

from src.api.user import get_current_user
from src.crud.task import get_tasks_of_project, create_task, delete_task, update_task, get_task_of_project
from src.schemas.info import ResponseInfo
from src.schemas.task import Task, TaskOut
from src.models.models import TaskModel
from src.schemas.user import UserOut

router = APIRouter()


@router.get(
    "/tasks/{project_id}/{task_id}",
    response_model=TaskOut,
    responses={401: {"model": ResponseInfo}}
)
def get_task_of_project_handler(project_id: int, task_id: int, current_user: UserOut = Depends(get_current_user)):
    return get_task_of_project(project_id, task_id, current_user.id)


@router.get(
    "/tasks/{project_id}",
    response_model=List[TaskOut],
    responses={401: {"model": ResponseInfo}}
)
def get_tasks_of_project_handler(project_id: int, current_user: UserOut = Depends(get_current_user)):
    return get_tasks_of_project(project_id, current_user.id)


@router.post(
    "/tasks/{project_id}/add",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def create_task_handler(project_id: int, task: Task, current_user: UserOut = Depends(get_current_user)):
    return create_task(project_id, task, current_user.id)


@router.delete(
    "/tasks/{project_id}/{task_id}",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def delete_task_handler(project_id: int, task_id: int, current_user: UserOut = Depends(get_current_user)):
    return delete_task(project_id, task_id, current_user.id)


@router.put(
    "/tasks/{project_id}/{task_id}",
    response_model=bool,
    responses={401: {"model": ResponseInfo}}
)
def update_task_handler(project_id: int, task_id: int, task: Task, current_user: UserOut = Depends(get_current_user)):
    return update_task(project_id, task_id, task, current_user.id)
