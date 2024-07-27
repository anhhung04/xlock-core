from pydantic import BaseModel
from typing import Optional, List

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

class ListItemsResponseModel(BaseModel):
    items: List[ItemModel]


class ItemResponseModel(BaseModel):
    item: ItemModel

class UpdateItemModel(BaseModel):
    name: Optional[str] = None
    site: Optional[str] = None
    description: Optional[str] = None
    credentials: Optional[str] = None
    logo_url: Optional[str] = None