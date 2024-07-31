from pydantic import Field, BaseModel
from models.user import QueryUserModel
from models.item import ItemModel, CreateItemModel
from typing import List
from models.response import BaseResponseModel


class ShareRequest(BaseModel):
    item_id: str
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
    item_id: str
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

class ShareItemModel(ItemModel):
    enc_pri: str
    shared_at: str
    shared_by: str
    type: str = Field(..., examples=["shared-item"])

class ItemListResponse(BaseResponseModel):
    data: List[ItemModel | ShareItemModel]

class ShareResponseModel(BaseResponseModel):
    data: ShareResponse