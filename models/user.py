from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserDetail(BaseModel):
    name: str
    email: EmailStr
    id: str
    registered_time: str
    update_time: str


class UserDetailResponse(UserDetail):
    data: UserDetail


class AddUserDetailModel(UserDetail):
    password: str


class AddUserModel(BaseModel):
    name: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_]{7,29}$")
    email: EmailStr
    id: str
    registered_time: str
    update_time: str


class PatchUserDetailModel(BaseModel):
    name: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    password: Optional[str] | None = None
    update_time: str


class PatchUserPrivateInfoModel(PatchUserDetailModel):
    password: Optional[str] | None = None
    name: Optional[str] | None = None
