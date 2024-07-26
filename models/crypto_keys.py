from pydantic import BaseModel
from uuid import UUID


class CryptoKeysModel(BaseModel):
    id: UUID
    user_id: UUID
    encrypt_key_pair: str
    salt: str
