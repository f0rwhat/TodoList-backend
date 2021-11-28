from sqlite3 import IntegrityError
from typing import List

from fastapi_sqlalchemy import db
from pydantic import EmailStr

from src.crud.user import get_user_by_email
from src.exceptions import UniqueDataException, ProjectNotFoundException, UnauthorizedAccess, UserNotFoundException, \
    UserNotInProjectException, UserIsAlreadyInProjectException, CantDeleteMaintainerFromProjectException
from src.models.models import ProjectModel, UsersProjectsModel, UserModel
from src.schemas.project import ProjectOut, Project
from src.schemas.user import UserBase


def check_user_is_in_project(project_id: int, user_id: int):
    db_project = (
        db.session.query(UsersProjectsModel)
            .filter(UsersProjectsModel.project_id == project_id)
            .filter(UsersProjectsModel.user_id == user_id)
            .first()
    )
    if db_project is None:
        db_project = (
            db.session.query(ProjectModel)
                .filter(ProjectModel.id == project_id)
                .first()
        )
        if db_project is None:
            raise ProjectNotFoundException()
        else:
            raise UnauthorizedAccess()


def check_user_is_maintainer(project_id: int, user_id: int):
    db_project = (
        db.session.query(ProjectModel)
            .filter(ProjectModel.id == project_id)
            .filter(ProjectModel.maintainer_id == user_id)
            .first()
    )
    if db_project is None:
        raise UnauthorizedAccess()


def get_project(project_id: int, user_id: int) -> ProjectOut:
    projects_users_db = (
        db.session.query(UsersProjectsModel)
            .filter(UsersProjectsModel.project_id == project_id)
            .filter(UsersProjectsModel.user_id == user_id)
            .first()
    )

    project_db = (
        db.session.query(ProjectModel)
            .filter(ProjectModel.id == project_id)
            .first()
    )

    if projects_users_db is None:
        if project_db is None:
            raise ProjectNotFoundException()
        else:
            raise UnauthorizedAccess()

    maintainer_db = (
        db.session.query(UserModel)
            .filter(UserModel.id == project_db.maintainer_id)
            .first()
    )
    result = ProjectOut(
                id=project_db.id,
                title=project_db.title,
                description=project_db.description,
                maintainer_name=maintainer_db.name
            )
    return result


def get_projects_of_user(user_id: int) -> List[ProjectOut]:
    projects_ids = (
        db.session.query(UsersProjectsModel)
            .filter(UsersProjectsModel.user_id == user_id)
            .all()
    )

    if projects_ids is None:
        raise ProjectNotFoundException()

    projects = []
    for project_id in projects_ids:
        project: ProjectModel = (
            db.session.query(ProjectModel)
                .filter(ProjectModel.id == project_id.project_id)
                .first()
        )
        maintainer = (
            db.session.query(UserModel)
                .filter(UserModel.id == project.maintainer_id)
                .first()
        )
        projects.append(
            ProjectOut(
                id=project.id,
                title=project.title,
                description=project.description,
                maintainer_name=maintainer.name
            )
        )
    return projects


def create_new_project(project: Project, user_id: int) -> bool:
    db_project = ProjectModel(
        title=project.title,
        description=project.description,
        maintainer_id=user_id
    )
    try:
        db.session.add(db_project)
        db.session.commit()

        db_user_project_link = UsersProjectsModel(
            user_id=user_id,
            project_id=db_project.id
        )
        db.session.add(db_user_project_link)
        db.session.commit()
    except IntegrityError as e:
        if isinstance(e.orig):
            db.session.rollback()
            raise UniqueDataException()
    return True


def delete_project(project_id: int, user_id: int) -> bool:
    db_project = (
        db.session.query(ProjectModel)
            .filter(ProjectModel.id == project_id)
            .first()
    )

    if db_project is None:
        raise ProjectNotFoundException()
    if db_project.maintainer_id != user_id:
        raise UnauthorizedAccess()

    db.session.delete(db_project)
    db.session.commit()
    return True


def update_project_info(project_id: int, project: Project, user_id: int) -> bool:
    db_project = (
        db.session.query(ProjectModel)
            .filter(ProjectModel.id == project_id)
            .first()
    )

    if db_project is None:
        raise ProjectNotFoundException()
    if db_project.maintainer_id != user_id:
        raise UnauthorizedAccess()

    db_project.title = project.title
    db_project.description = project.description
    db.session.commit()
    return True


def get_users_of_project(project_id: int, caller_user_id: int) -> List[UserBase]:
    check_user_is_maintainer(project_id, caller_user_id)
    dbs_users_projects = (
        db.session.query(UsersProjectsModel)
            .filter(UsersProjectsModel.project_id == project_id)
            .all()
    )
    users = []
    for db_user_project in dbs_users_projects:
        user: UserBase = (
            db.session.query(UserModel)
                .filter(UserModel.id == db_user_project.user_id)
                .first()
        )
        users.append(user)
    return users


def add_user_to_project(project_id: int, email: EmailStr, caller_user_id: int) -> bool:
    db_project = (
        db.session.query(ProjectModel)
            .filter(ProjectModel.id == project_id)
            .first()
    )
    if db_project is None:
        raise ProjectNotFoundException()
    if db_project.maintainer_id != caller_user_id:
        raise UnauthorizedAccess()

    db_user = get_user_by_email(email)
    if db_user is None:
        raise UserNotFoundException()

    db_access = (
        db.session.query(UsersProjectsModel)
            .filter(UsersProjectsModel.user_id == db_user.id)
            .filter(UsersProjectsModel.project_id == project_id)
            .first()
    )
    if db_access is None:
        db_access = UsersProjectsModel(user_id=db_user.id, project_id=project_id)
        db.session.add(db_access)
        db.session.commit()
    else:
        raise UserIsAlreadyInProjectException()


    return True


def delete_user_from_project(project_id: int, email: EmailStr, caller_user_id: int) -> bool:
    db_project = (
        db.session.query(ProjectModel)
            .filter(ProjectModel.id == project_id)
            .first()
    )

    if db_project is None:
        raise ProjectNotFoundException()
    if db_project.maintainer_id != caller_user_id:
        raise UnauthorizedAccess()

    db_user = get_user_by_email(email)
    if db_user is None:
        raise UserNotFoundException()

    if db_user.id == db_project.maintainer_id:
        raise CantDeleteMaintainerFromProjectException()
    print('Deleting from project' + email + '==' + db_user.email)
    db_access = (
        db.session.query(UsersProjectsModel)
            .filter(UsersProjectsModel.project_id == project_id)
            .filter(UsersProjectsModel.user_id == db_user.id)
            .first()
    )

    if db_access is None:
        raise UserNotInProjectException()

    db.session.delete(db_access)
    db.session.commit()
    return True