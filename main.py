import uvicorn
from fastapi import FastAPI, Request
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.responses import JSONResponse

from src.api import task, user, projects, priorities
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from src.exceptions import GenericException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(task.router)
app.include_router(user.router)
app.include_router(projects.router)
app.include_router(priorities.router)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(GenericException)
async def exception_handler(request: Request, exc: GenericException):
    return JSONResponse(status_code=exc.code, content={"msg": exc.msg})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
