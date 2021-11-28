from pydantic import BaseModel, Field, validator
from typing import Optional


class Project(BaseModel):
    title: str
    description: Optional[str] = Field(None)

    class Config:
        orm_mode = True

    @validator('title')
    def phone_validator(cls, v):
        if v is None:
            raise ValueError("Имя проекта не может быть пустым!")
        return v


class ProjectOut(Project):
    id: int
    maintainer_name: str
