from fastapi import Depends
from . import Storage
from typing import List
from .schemas.item import *  # noqa: F403
from .schemas.user import *  # noqa: F403
from models.item import *  # noqa: F403
from uuid import uuid4


class ItemRepository:
    def __init__(self, storage: Storage = Depends(Storage)):
        self._sess = storage._db

    async def list(self, site: str) -> List[Item]:  # noqa: F405
        items = await self._sess.query(Item).filter(Item.site == site).all()  # noqa: F405
        return items

    async def add(self, item: ItemModel, user_id: str) -> PersonalItem:  # noqa: F405
        itemAsDict = item.model_dump()
        itemAsDict.update({"id": uuid4(), "owner_id": user_id})
        personalItem = PersonalItem(**itemAsDict)  # noqa: F405
        self._sess.add(personalItem)
        self._sess.commit()
        self._sess.refresh(personalItem)
        return personalItem
