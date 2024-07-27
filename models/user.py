from pydantic import BaseModel, EmailStr
from typing import Optional


class RSAKeyPair(BaseModel):
    public: str
    enc_pri: str
    salt: str

class UserDetail(BaseModel):
    id: str
    name: str
    email: EmailStr

class GetUserDetail(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: str
    updated_at: Optional[str] = None

class UserDetailResponse(UserDetail):
    data: UserDetail

class UserDetailWithKey(UserDetail):
    rsa_key_pair: RSAKeyPair

class UserDetailWithKeyResponse(UserDetailWithKey):
    data: UserDetailWithKey

class CreateUserModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    rsa_key_pair: RSAKeyPair
    
class QueryUserModel(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    email: Optional[EmailStr] = None

class UpdateUserModel(BaseModel):
    name: Optional[str] = None

