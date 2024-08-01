from pydantic import BaseModel, field_validator, Field
from typing import Optional
from models.response import BaseResponseModel
from datetime import datetime
from uuid import UUID

class CreateItemModel(BaseModel):
    name: str = Field(..., examples=["Facebook"])
    site: str = Field(..., examples=["https://www.facebook.com"])
    description: Optional[str] = None
    enc_credentials: str = Field(..., description="Encrypted value of credentials")
    logo_url: Optional[str] = None

class ItemModel(CreateItemModel):
    id: UUID
    added_at: datetime = Field(..., examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")
    type: str = Field(..., description="Type of item (personal_item / shared_item / group_item)", examples=["personal-item"])
    updated_at: Optional[datetime] = Field(None, examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ItemDetailResponse(BaseResponseModel):
    data: ItemModel

class DeleteItemResponse(BaseResponseModel):
    data: None

class UpdateItemModel(BaseModel):
    name: Optional[str] = None
    site: Optional[str] = None
    description: Optional[str] = None
    enc_credentials: Optional[str] = None
    logo_url: Optional[str] = None