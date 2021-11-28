from fastapi import APIRouter
from typing import List

from src.crud.priorities import get_priorities
from src.schemas.info import ResponseInfo
from src.schemas.priority import PriorityOut

router = APIRouter()


@router.get(
    "/priorities",
    response_model=List[PriorityOut],
    responses={401: {"model": ResponseInfo}}
)
def get_priorities_handler():
    return get_priorities()
