from fastapi import Depends
from repository import Storage
from repository.schemas.user import *
from models.user import *
from uuid import uuid4


class UserRepository:
    def __init__(self, storage: Storage = Depends(Storage)):
        self._sess = storage._db

    async def add(self, newUser: NewUserDetailModel) -> User:
        newUser = User(
            name=newUser.name,
            email=newUser.email,
            password=newUser.password,
            key=CryptoKey(
                public_key=newUser.rsa_key_pair.public,
                private_key=newUser.rsa_key_pair.enc_pri,
                salt=newUser.rsa_key_pair.salt,
            )
        )
        try:
            self._sess.add(newUser)
            self._sess.commit()
            self._sess.refresh(newUser)
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return newUser

    async def get(self, query: QueryUserModel) -> User:
        try:
            existUser = (
                self._sess.query(User)
                .filter_by(**query.model_dump(exclude_none=True))
                .first()
            )
        except Exception as e:
            raise Exception(e)
        return existUser
