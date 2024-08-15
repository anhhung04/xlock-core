from pydantic import BaseModel, Field
from models.response import BaseResponseModel
from typing import Optional


class UserAuth(BaseModel):
    identity: str = Field(
        ..., description="User email or username", max_length=50, min_length=3
    )
    password: str = Field(
        ...,
        description="User password",
        max_length=128,
        min_length=8,
        pattern="^[a-z0-9]+$",
    )


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

class CrytoKey(BaseModel):
    public_key: str
    enc_pri: Optional[str] = None

class CrytoKeyResponse(BaseResponseModel):
    data: CrytoKey
