from typing import List

from fastapi_sqlalchemy import db

from src.crud.projects import check_user_is_in_project
from src.exceptions import ProjectNotFoundException, UnauthorizedAccess, TaskNotFoundException
from src.models.models import TaskModel, UsersProjectsModel, ProjectModel
from src.schemas.task import Task, TaskOut


def get_task_of_project( project_id: int, task_id: int, user_id: int) -> TaskOut:
    check_user_is_in_project(project_id, user_id)
    tasks = (
        db.session.query(TaskModel)
            .filter(TaskModel.project_id == project_id)
            .filter(TaskModel.id == task_id)
            .first()
    )
    return tasks


def get_tasks_of_project(project_id: int, user_id: int) -> List[TaskOut]:
    check_user_is_in_project(project_id, user_id)
    tasks = (
        db.session.query(TaskModel)
            .filter(TaskModel.project_id == project_id)
            .all()
    )
    return tasks


def create_task(project_id: int, task: Task, user_id: int) -> bool:
    check_user_is_in_project(project_id, user_id)
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        project_id=project_id,
        priority_id=task.priority_id
    )
    db.session.add(db_task)
    db.session.commit()
    return True


def delete_task(project_id: int, task_id: int, user_id: int) -> bool:
    check_user_is_in_project(project_id, user_id)
    db_task = (
        db.session.query(TaskModel)
            .filter(TaskModel.id == task_id)
            .filter(TaskModel.project_id == project_id)
            .first()
    )
    if db_task is None:
        raise TaskNotFoundException()
    db.session.delete(db_task)
    db.session.commit()
    return True


def update_task(project_id: int, task_id: int, task: Task, user_id: int) -> bool:
    check_user_is_in_project(project_id, user_id)
    db_task = (
        db.session.query(TaskModel)
            .filter(TaskModel.id == task_id)
            .filter(TaskModel.project_id == project_id)
            .first()
    )
    if db_task is None:
        raise TaskNotFoundException()

    db_task.title = task.title
    db_task.description = task.description
    db_task.priority_id = task.priority_id
    db.session.commit()
    return True