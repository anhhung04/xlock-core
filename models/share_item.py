from pydantic import Field, BaseModel
from models.user import QueryUserModel
from models.item import ItemModel, CreateItemModel
from typing import List
from models.response import BaseResponseModel
from datetime import datetime
from uuid import UUID

class ShareRequest(BaseModel):
    item_id: UUID
    recipient: QueryUserModel = Field(
        ...,
        description="info of object be shared with",
        examples=[{"email": "user1@gmail.com"}],
    )


class ShareResponse(BaseModel):
    type: str = Field(..., examples=["shared_item"])
    enc_credentials: str = Field(
        ..., description=("encrypted by pass of owner or public key of owner")
    )
    enc_pri: str = Field(..., description=("encrypted by pass of owner"))
    recipient_pub: str


class CreateShareItem(BaseModel):
    item_id: UUID
    enc_credentials: str = Field(
        ..., description=("encrypted by public key of recipient")
    )
    recipient: QueryUserModel = Field(
        ...,
        description="username | email | id of recipient (must be 1 in 3)",
        examples=[{"email": "user1@gmail.com"}],
    )

class AddShareItem(CreateItemModel):
    enc_pri: str = Field(..., description=("encrypted by pass of owner"))

class ShareItemActor(BaseModel):
    id: str
    username: str
    email: str

class ShareItemModel(ItemModel):
    enc_pri: str
    shared_at: datetime = Field(..., examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")
    type: str = Field(..., examples=["shared_item"])

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }

class ShareItemElement(ItemModel):
    enc_credentials: str
    shared_at: datetime = Field(..., examples=["2024-08-16 00:00:00"], description="Date time in format YYYY-MM-DD HH:MM:SS")
    type: str = Field(..., examples=["shared_item"])
    shared_by: ShareItemActor

class ItemListResponse(BaseResponseModel):
    data: List[ItemModel | ShareItemElement]

class ShareResponseModel(BaseResponseModel):
    data: ShareResponse