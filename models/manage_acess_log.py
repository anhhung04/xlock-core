from pydantic import BaseModel
from uuid import UUID


class ManageAccessLogModel(BaseModel):
    id: str
    user_id: UUID
    action: str
    time: str
    status: str
    location: str
    user_agent: str
    device_id: str
    ip: str
