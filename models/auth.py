from pydantic import BaseModel
from models.response import BaseResponseModel
from typing import Optional


class UserAuth(BaseModel):
    name: Optional[str] | None = None
    email: Optional[str] | None = None
    password: str


class VerifyTokenRequest(BaseModel):
    access_token: str


class AcessResponse(BaseModel):
    access_token: str


class UserAuthResponse(BaseResponseModel):
    data: AcessResponse


class VerifyUserReponseData(BaseModel):
    is_login: bool
    name: str
    user_id: str


class VerifyTokenReponse(BaseResponseModel):
    data: VerifyUserReponseData


class LogoutData(BaseModel):
    success: bool


class LogoutResponseModel(BaseResponseModel):
    data: LogoutData
