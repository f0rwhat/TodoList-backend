from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class PriorityModel(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    tasks = relationship("TaskModel", back_populates="priority", cascade='all,delete')


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    maintainer_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)

    tasks = relationship("TaskModel", back_populates="project", cascade='all,delete')
    users = relationship("UsersProjectsModel", back_populates="project", cascade='all,delete')
    maintainer = relationship("UserModel", back_populates="maintainer")


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    priority_id = Column(Integer, ForeignKey('priorities.id'))
    title = Column(String)
    description = Column(String)

    priority = relationship("PriorityModel", back_populates="tasks")
    project = relationship("ProjectModel", back_populates="tasks")


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    projects = relationship("UsersProjectsModel", back_populates="user", cascade='all,delete')
    maintainer = relationship("ProjectModel", back_populates="maintainer", cascade='all, delete')


class UsersProjectsModel(Base):
    __tablename__ = "users_projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    user = relationship("UserModel", back_populates="projects")
    project = relationship("ProjectModel", back_populates="users", cascade='all,delete')
