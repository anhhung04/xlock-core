from fastapi import Depends
from repository import Storage
from repository.schemas.user import *
from models.user import *
from uuid import uuid4


class UserRepository:
    def __init__(self, storage: Storage = Depends(Storage)):
        self._sess = storage._db

    async def add(self, newUser: NewUserDetailModel) -> UserDetail:
        newUserAsDict = newUser.model_dump()
        newUserAsDict.update(
            {
                "id": uuid4(),
            }
        )
        newUser = User(**newUserAsDict)
        try:
            self._sess.add(newUser)
            self._sess.commit()
            self._sess.refresh(newUser)
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return UserDetail.model_validate(newUser, strict=False, from_attributes=True)

    async def get(self, query: QueryUserModel) -> UserDetail:
        existUser = (
            self._sess.query(User)
            .filter_by(**query.model_dump(exclude_none=True))
            .first()
        )
        assert existUser, "User not found"
        return UserDetail.model_validate(existUser, from_attributes=True)
