from fastapi.responses import JSONResponse
from fastapi import Depends, Cookie, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from repository import Storage
from typing import Optional, Annotated
from redis import Redis
from jwt import encode, decode
from string import ascii_letters, digits
from random import choices
from repository.schemas.user import User
from utils.log import logger


class JWTHandler:
    def __init__(self, secret_store: Redis):
        self._secret_store = secret_store

    def gen(self, payload: dict) -> str:
        assert "id" in payload, "Payload must contain id"
        secret: str = ''.join(choices(ascii_letters + digits, k=64))
        self._secret_store.set(payload["id"], secret)
        return encode(payload, secret, algorithm="HS256")

    def verify(self, token: str) -> dict:
        payload = decode(token, options={"verify_signature": False})
        secret = self._secret_store.get(payload["id"])
        return decode(token, secret, algorithms="HS256")


class APIResponse:
    @staticmethod
    def as_json(status_code: int, message: str, data: dict | None = None):
        content = {
            "code": status_code,
            "status": message,
        }
        if data is not None:
            content.update({"data": data})
        return JSONResponse(content=content, status_code=status_code)

header = HTTPBearer(
    auto_error=False,
    scheme_name="Bearer",
)

class UserSession:
    def __init__(
        self,
        storage: Storage = Depends(Storage),
        auth_cookie: Optional[str] = Cookie(None, alias="auth"),
        auth_header: Annotated[HTTPAuthorizationCredentials, "Authorization header"] = Depends(header),
    ):
        try:
            self._token = auth_cookie or auth_header.credentials            
            self._db = storage._db
            self._jwt = JWTHandler(storage._fstore)
            self._user_id = self._jwt.verify(self._token)["id"]
            self._user = self._db.query(User).filter(User.id == self._user_id).first()
        except Exception:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
