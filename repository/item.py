from fastapi import Depends
from . import Storage
from typing import List
from .schemas.item import *  
from .schemas.user import *  
from models.item import * 
from uuid import uuid4


class ItemRepository:
    def __init__(self, storage: Storage = Depends(Storage)):
        self._sess = storage._db

    async def list(self, site: str) -> List[Item]: 
        items = await self._sess.query(Item).filter(Item.site == site).all()  
        return items

    async def add(self, item: AddItemModel, user_id: str) -> PersonalItem:  
        personalItem = PersonalItem(
            name=item.name,
            site=item.site,
            description=item.description,
            credentials=item.credentials,
            owner_id=user_id,
        ) 
        self._sess.add(personalItem)
        self._sess.commit()
        self._sess.refresh(personalItem)
        return personalItem
