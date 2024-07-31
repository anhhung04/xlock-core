from typing import List, Optional

from pydantic import BaseModel

from models.response import BaseResponseModel


class CreateItemModel(BaseModel):
    name: str
    site: str
    description: str
    credentials: str
    logo_url: Optional[str] = None


class ItemModel(CreateItemModel):
    id: str
    added_at: str
    type: str
    updated_at: Optional[str] = None
    logo_url: Optional[str] = None


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
