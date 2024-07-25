from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemsDetail(BaseModel):
    id: str
    user_id: str
    name: str
    credentials: str  # after encryption
    url: str
    logo_url: str
    description: str
    type: str
    added_time: datetime
    last_modified_time: datetime


class ItemCreateDTO(BaseModel):
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    encrypted_credential: Optional[str] = None
    added_time: datetime
    user_id: str


class ItemReadDTO(BaseModel):
    id: str
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    encrypted_credential: Optional[str] = None
    added_time: datetime
    last_modified_time: datetime
    user_id: str


class ItemUpdateDTO(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    encrypted_credential: Optional[str] = None
    last_modified_time: datetime


class ItemDeleteDTO(BaseModel):
    id: str
