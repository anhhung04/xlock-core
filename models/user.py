from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserDetail(BaseModel):
    name: str
    email: EmailStr
    id: UUID
    registered_time: str
    update_time: str


class UserDetailResponse(UserDetail):
    data: UserDetail


class AddUserDetailModel(UserDetail):
    password: str


class AddUserModel(BaseModel):
    name: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_]{7,29}$")
    email: EmailStr
    id: UUID
    registered_time: str
    update_time: str


class QueryUserModel(BaseModel):
    name: str
    id: UUID
    email: EmailStr
