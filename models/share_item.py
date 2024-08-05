from pydantic import Field, BaseModel, EmailStr

from models.item import ItemModel, CreateItemModel
from models.response import BaseResponseModel

from datetime import datetime
from typing import List
from uuid import UUID

from utils.validate import ValidateInput

class BaseShareModel(BaseModel):
    item_id: UUID
    recipient: EmailStr | UUID | str = Field(..., description="email; id; username of recipient (must be 1 in 3)")

    def validate_recipient(self) -> dict[str, str]:
        input = self.recipient
        if ValidateInput.is_email(input):
            return {"email": input}
        elif ValidateInput.is_uuid(input):
            return {"id": input}
        elif isinstance(input, str):
            return {"username": input}
        else:
            raise ValueError("Invalid recipient input")

class ShareRequest(BaseShareModel):
    pass

class ShareResponse(BaseModel):
    type: str = Field(..., examples=["shared_item"])
    enc_credentials: str = Field(
        ..., description=("encrypted by pass of owner or public key of owner")
    )
    enc_pri: str = Field(..., description=("encrypted by pass of owner"))
    recipient_pub: str

class CreateShareItem(BaseShareModel):
    enc_credentials: str = Field(
        ..., description=("encrypted by public key of recipient")
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