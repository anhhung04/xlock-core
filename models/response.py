from pydantic import BaseModel
from typing import Optional


class BaseResponseModel(BaseModel):
    code: int
    status: str
    data: Optional[dict] = None
