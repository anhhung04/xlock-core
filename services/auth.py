from fastapi import Depends
from repository.user import UserRepository
from repository import Storage
from models.user import *
from models.auth import *
from hashlib import pbkdf2_hmac
from config import config
from utils.http import JWTHandler

class PasswordProcesser:
    def __init__(self, raw_pass: str, salt):
        self._raw = raw_pass
        self._salt = salt
        self._ITERATIONS = 10000

    def hash(self):
        return pbkdf2_hmac(
            "sha256",
            self._raw.encode("utf-8"),
            self._salt.encode("utf-8"),
            self._ITERATIONS,
        ).hex()

    def verify(self, hashed_pass: str):
        return self.hash() == hashed_pass


class AuthService:
    def __init__(
        self,
        repo: UserRepository = Depends(UserRepository),
        storage: Storage = Depends(Storage),
    ):
        self._repo = repo
        self._jwt = JWTHandler(storage._fstore)

    async def create_user(self, newUser: NewUserDetailModel):
        existUser = await self._repo.get(newUser.username)
        if existUser:
            raise Exception("User already exists")
        newUser.password = PasswordProcesser(newUser.password, config.SALT).hash()
        return await self._repo.add(newUser)

    async def verify(self, authInfo: UserAuth) -> AccessResponse:
        existUser = await self._repo.get(authInfo.email)
        assert existUser, "User does not exist"
        assert PasswordProcesser(authInfo.password, config.SALT).verify(
            existUser.password
        ), "Password does not match"
        return self._jwt.gen({"id": existUser.id})

    async def verify(self, email: str) -> IsValidToken:
        return IsValidToken(is_valid=self._jwt.verify(email) is not None)

    async def log(self, email: str):
        pass
