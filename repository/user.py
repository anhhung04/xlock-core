from fastapi import Depends

from repository import Storage
from repository.schemas.user import *

from models.user import *

from uuid import uuid4


class UserRepository:
    def __init__(self, storage: Storage = Depends(Storage)):
        self._sess = storage._db

    async def add(self, newUser: CreateUserModel) -> User:
        newUser = User(
            username=newUser.username,
            email=newUser.email,
            password=newUser.password,
            fullname=newUser.fullname,
            dob=newUser.dob,
            address=newUser.address,
            phone_number=newUser.phone_number,
            country=newUser.country,
            gender=newUser.gender,
            backup_email=newUser.backup_email,
            key=CryptoKey(
                public_key=newUser.rsa_key_pair.public,
                enc_pri=newUser.rsa_key_pair.enc_pri,
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
    
    async def update(self, id: str, userInfo: UpdateUserModel) -> User:
        try:
            user = self._sess.query(User).filter(User.id == id).first()
            if user:
                for key, value in userInfo.model_dump(exclude_none=True).items(): 
                    setattr(user, key, value)
                self._sess.commit()
                self._sess.refresh(user)
            else:
                raise Exception("User not found")
        except Exception as e:
            raise Exception(e)
        return user
    
    async def delete(self, id: str) -> None:
        try:
            user = self._sess.query(User).filter(User.id == id).first()
            if user:
                self._sess.delete(user)
                self._sess.commit()
            else:
                raise Exception("User not found")
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return None


