from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    code: int
    status: str
    data: dict
