from fastapi import Depends
from fastapi.exceptions import HTTPException
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

    async def create(self, newUser: NewUserDetailModel) -> dict:
        existUser = await self._repo.get(QueryUserModel(email=newUser.email))
        if existUser:
            raise HTTPException(status_code=409, detail="User already exists")
        newUser.password = PasswordProcesser(newUser.password, config["SALT"]).hash()
        user = await self._repo.add(newUser)
        return UserDetail(
            id=str(user.id),
            name=user.name,
            email=user.email,
        ).model_dump()

    async def gen_token(self, authInfo: UserAuth) -> dict:
        existUser = await self._repo.get(QueryUserModel(email=authInfo.email))
        if not existUser:
            raise HTTPException(status_code=404, detail="User does not exist")
        return AccessResponse(
            access_token=self._jwt.gen({"id": str(existUser.id)})
        ).model_dump()

    async def verify(self, email: str) -> dict:
        return IsValidToken(is_valid=self._jwt.verify(email) is not None).model_dump()

    async def log(self, email: str):
        pass
