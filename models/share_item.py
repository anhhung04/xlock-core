from pydantic import Field

from models.user import QueryUserModel


class ShareRequest:
    item_id: str
    recipient: QueryUserModel = Field(
        ...,
        description="info of object be shared with",
        examples=[{"email": "user1@gmail.com"}],
    )


class ShareResponse:
    type: str = Field(..., examples=["shared_item"])
    enc_credentials: str = Field(
        ..., description=("encrypted by pass of owner or public key of owner")
    )
    enc_pri: str = Field(..., description=("encrypted by pass of owner"))
    recipient_pub: str


class CreateShareItem:
    item_id: str
    enc_credentials: str = Field(
        ..., description=("encrypted by public key of recipient")
    )
    recipient: QueryUserModel = Field(
        ...,
        description="username or email or id of recipient",
        examples=["user1@gmai.com"],
    )
