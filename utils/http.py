from fastapi.responses import JSONResponse
from fastapi import Depends, Cookie, Header
from repository import Storage
from typing import Optional
from redis import Redis
from jwt import encode, decode
from string import ascii_letters, digits
from random import choices
from repository.schemas.user import User


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


class UserSession:
    def __init__(
        self,
        storage: Storage = Depends(Storage),
        auth_cookie: Optional[str] = Cookie(alias="auth"),
        auth_header: Optional[str] = Header(alias="Authorization"),
    ):
        self._token = auth_cookie or auth_header
        assert self._sess is not None, "Please provide a valid token"
        self._db = storage._db
        self._jwt = JWTHandler(storage._fstore)
        self._user_id = self._jwt.verify(self._token)["id"]
        self._user = self._db.query(User).filter(User.id == self._user_id).first()
        assert self._user is not None, "User does not exist"
