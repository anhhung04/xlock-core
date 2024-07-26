from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    code: int
    status: str
    data: dict

    class Config:
        fields = {
            "code": "status_code",
            "status": "message",
        }
