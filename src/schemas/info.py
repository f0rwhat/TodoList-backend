from pydantic import BaseModel


class ResponseInfo(BaseModel):
    msg: str

    class Config:
        orm_mode = True


class NotVerifiedScheme(BaseModel):
    msg: str
    verification_token: str

    class Config:
        orm_mode = True
