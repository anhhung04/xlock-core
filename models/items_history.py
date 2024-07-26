from pydantic import BaseModel
from uuid import UUID


class ItemHistoryDetail(BaseModel):
    id: str
    user_id: UUID
    action: str
    status: str
    name: str
    credentials: str
    url: str
    logo_url: str
    description: str
    added_time: str
    last_modified_time: str
    user_agent: str
    device_id: str


class SharingHistoryDTO(ItemHistoryDetail):
    item_history_id: UUID
    recipient_id: UUID

    class Config:
        orm_mode = True


class FillingHistoryDTO(ItemHistoryDetail):
    item_history_id: UUID

    class Config:
        orm_mode = True
