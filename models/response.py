from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    status_code: int
    message: str
    data: dict

    def as_json(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
        }
