from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


class UserDetail(BaseModel):
    name: str
    email: EmailStr
    id: UUID
    update_at: datetime
    create_at: datetime


class UserDetailResponse(UserDetail):
    data: UserDetail


class AddUserDetailModel(UserDetail):
    password: str


class AddUserModel(BaseModel):
    name: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_]{7,29}$")
    email: EmailStr
    id: UUID
    update_at: datetime
    create_at: datetime


class QueryUserModel(BaseModel):
    name: str
    id: UUID
    email: EmailStr
