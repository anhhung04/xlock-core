from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ItemsDetailModel(BaseModel):
    id: UUID
    user_id: str
    name: str
    credentials: str
    url: str
    logo_url: str
    description: str
    type: str
    added_time: datetime
    last_modified_time: datetime


class AddItemsModel(BaseModel):
    id: str
    name: str
    url: str
    description: str
    type: str
    credentials: str
    added_time: datetime
    user_id: str


class PatchItemsDetailModel(BaseModel):
    id: str
    user_id: UUID
    name: str
    credentials: str
    url: str
    type: str
    added_time: datetime
    last_modified_time: datetime


class DeleteItemModel(BaseModel):
    id: str
    user_id: UUID


class ShareAccountModel(ItemsDetailModel):
    share_time: datetime
    private_key: str
    id: str


class OriginalAccountModel(ItemsDetailModel):
    id: str
