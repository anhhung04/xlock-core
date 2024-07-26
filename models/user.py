from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class RSAKeyPair(BaseModel):
    public: str
    enc_pri: str
    salt: str


class UserDetail(BaseModel):
    name: str
    email: EmailStr


class UserDetailResponse(UserDetail):
    data: UserDetail


class UserDetailWithKey(UserDetail):
    rsa_key_pair: RSAKeyPair


class UserDetailWithKeyResponse(UserDetailWithKey):
    data: UserDetailWithKey


class NewUserDetailModel(UserDetailWithKey):
    password: str


class QueryUserModel(BaseModel):
    name: Optional[str] = None
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
