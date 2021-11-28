from pydantic import BaseModel, Field, validator
from typing import Optional


class Priority(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator('name')
    def phone_validator(cls, v):
        if v is None:
            raise ValueError("Название приоритета не может быть пустым!")
        return v


class PriorityOut(Priority):
    id: int
