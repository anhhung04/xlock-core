from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from redis import Redis
from jwt import encode, decode
from string import ascii_letters, digits
from random import choices
from hashlib import pbkdf2_hmac
from config import config
import time


class JWTHandler:
    def __init__(self, secret_store: Redis, expire: int = config["TOKEN_EXPIRE"]):
        self._secret_store = secret_store
        self._expire = expire

    def create_token(self, payload: dict) -> str:
        if "id" not in payload:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payload must contain 'id' field",
            )
        secret = self._secret_store.get(payload["id"])
        if not secret:
            secret = self.random_secret(64)
            self._secret_store.set(payload["id"], secret, ex=self._expire)
        secret = str(secret, "utf-8")
        payload["iat"] = payload.get("iat", time.time() // 1000)
        payload["issuer"] = payload.get("iss", "xlock")
        return encode(payload, secret, algorithm="HS256")

    def verify(self, token: str) -> dict:
        payload = decode(token, options={"verify_signature": False})
        secret = self._secret_store.get(payload["id"])
        try:
            if not secret:
                raise Exception("Cannot find secret")
            return decode(token, str(secret, "utf-8"), algorithms=["HS256"])
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired",
            )

    def revoke(self, token: str) -> None:
        payload = decode(token, options={"verify_signature": False})
        self._secret_store.delete(payload["id"])

    def refresh(self, token: str) -> str:
        payload = decode(token, options={"verify_signature": False})
        return self.create_token(payload)

    @staticmethod
    def random_secret(lenght: int = 32) -> str:
        alp = ascii_letters + digits
        return pbkdf2_hmac(
            "sha512", "".join(choices(alp, k=lenght)).encode(), b"", 100000
        ).hex()


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
