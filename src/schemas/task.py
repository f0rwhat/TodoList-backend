from pydantic import BaseModel, Field, validator
from typing import Optional


class Task(BaseModel):
    title: str
    description: Optional[str] = Field(None)
    priority_id: int

    class Config:
        orm_mode = True

    @validator('title')
    def phone_validator(cls, v):
        if v is None:
            raise ValueError("Заголовок задачи не может быть пустым!")
        return v


class TaskOut(Task):
    id: int
    project_id: int
