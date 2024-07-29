from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from models.response import BaseResponseModel
from datetime import date, datetime

class RSAKeyPair(BaseModel):
    public: str
    enc_pri: str
    salt: str

class GetUserDetail(BaseModel):
    id: str
    name: str
    email: EmailStr
    email2: Optional[EmailStr] = None
    fullname: str
    dob: str
    address: str    
    phone_number: str
    country: str
    gender: Optional[str] = None
    created_at: str = Field(..., examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")
    updated_at: Optional[str] = Field(default=None, examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")

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
    name: str = Field(..., description="Display name of user", examples=["mr.xlock"])
    email: EmailStr
    password: str
    fullname: str = Field(..., description="Full name of user", examples=["John Doe"])
    dob: date
    address: str    
    phone_number: str
    country: str
    gender: Optional[str] = None
    email2: Optional[EmailStr] = None
    rsa_key_pair: RSAKeyPair
    
class QueryUserModel(BaseModel):
    name: Optional[str] = None
    id: Optional[str] = None
    email: Optional[EmailStr] = None

class UpdateUserModel(BaseModel):
    name: Optional[str] = None
    fullname: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    gender: Optional[str] = None

