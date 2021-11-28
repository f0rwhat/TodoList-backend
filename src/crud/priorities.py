from typing import List

from fastapi_sqlalchemy import db

from src.models.models import PriorityModel
from src.schemas.priority import PriorityOut


def get_priorities() -> List[PriorityOut]:
    priorities = (
        db.session.query(PriorityModel)
            .all()
    )
    return priorities
