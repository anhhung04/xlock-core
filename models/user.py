from datetime import date, datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from models.response import BaseResponseModel


class RSAKeyPair(BaseModel):
    public: str
    enc_pri: str
    salt: str


class GetUserDetail(BaseModel):
    id: str
    username: str
    email: EmailStr
    backup_email: Optional[EmailStr] = None
    fullname: str
    dob: str
    address: str
    phone_number: str
    country: str
    gender: str
    created_at: str = Field(
        ...,
        examples=["2024-08-16 00:00:00"],
        description="Date time in format YYYY-MM-DD HH:MM:SS",
    )
    updated_at: Optional[str] = Field(
        default=None,
        examples=["2024-08-16 00:00:00"],
        description="Date time in format YYYY-MM-DD HH:MM:SS",
    )

    @field_validator("created_at", "updated_at", mode="after")
    def time_format(cls, v):
        if v is None:
            return None
        dt = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class UserDetailResponse(BaseResponseModel):
    data: GetUserDetail


class DeleteUserResponse(BaseResponseModel):
    data: None


class UserDetailWithKey(GetUserDetail):
    rsa_key_pair: RSAKeyPair


class UserDetailWithKeyResponse(BaseResponseModel):
    data: UserDetailWithKey


class CreateUserModel(BaseModel):
    username: str = Field(
        ..., description="Display name of user", examples=["mr.xlock"]
    )
    email: EmailStr
    password: str
    fullname: str = Field(
        ..., description="Full name of user", examples=["John Doe"]
    )
    dob: date
    address: str
    phone_number: str
    country: str
    gender: str
    backup_email: Optional[EmailStr] = None
    rsa_key_pair: RSAKeyPair


class QueryUserModel(BaseModel):
    username: Optional[str] = None
    id: Optional[str] = None
    email: Optional[EmailStr] = None

    @model_validator(mode="after")
    def check_null(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be filled")
        return values


class UpdateUserModel(BaseModel):
    username: Optional[str] = None
    fullname: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    gender: Optional[str] = None
