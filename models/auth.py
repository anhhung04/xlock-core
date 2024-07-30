from pydantic import BaseModel, EmailStr
from models.response import BaseResponseModel


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class VerifyTokenRequest(BaseModel):
    access_token: str


class IsValidToken(BaseModel):
    is_valid: bool


class VerifyTokenResponse(BaseResponseModel):
    data: IsValidToken


class AccessResponse(BaseModel):
    access_token: str


class UserAuthResponse(BaseResponseModel):
    data: AccessResponse
