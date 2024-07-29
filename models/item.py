from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from models.response import BaseResponseModel
from datetime import datetime

class CreateItemModel(BaseModel):
    name: str = Field(..., examples=["Facebook"])
    site: str = Field(..., examples=["https://www.facebook.com"])
    description: Optional[str] = None
    credentials: str = Field(..., description="Encrypted value of credentials")
    logo_url: Optional[str] = None

class ItemModel(CreateItemModel):
    id: str
    added_at: str = Field(..., examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")
    type: str = Field(..., description="Type of item (personal-item / shared-item / base-item)", examples=["personal-item"])
    updated_at: Optional[str] = None
    logo_url: Optional[str] = None

    @field_validator("added_at", "updated_at", mode="after")
    def time_format(cls, v):
        if v is None:
            return None
        dt = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
        return dt.strftime("%Y-%m-%d %H:%M:%S")

class ItemListResponse(BaseResponseModel):
    data: List[ItemModel]


class ItemDetailResponse(BaseResponseModel):
    data: ItemModel

class DeleteItemResponse(BaseResponseModel):
    data: None

class UpdateItemModel(BaseModel):
    name: Optional[str] = None
    site: Optional[str] = None
    description: Optional[str] = None
    credentials: Optional[str] = None
    logo_url: Optional[str] = None