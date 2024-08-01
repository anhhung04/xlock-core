from fastapi import Depends
from . import Storage
from typing import List
from .schemas.item import *  
from .schemas.user import *  
from models.item import * 
from models.share_item import *


class ItemRepository:
    def __init__(self, storage: Storage = Depends(Storage)):
        self._sess = storage._db

    async def list(self, id: str, site: str | None) -> List[PersonalItem | SharedItem]: 
        try:
            items = self._sess.query(Item).filter(Item.owner_id == id)
            items = items.filter(Item.site == site).all() if site else items.all()
        except Exception as e:
            raise Exception(e)
        return items

    async def add(self, item: PersonalItem | SharedItem) -> PersonalItem | SharedItem:
        try:
            self._sess.add(item)
            self._sess.commit()
            self._sess.refresh(item)
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return item
    
    async def update(self, item_id: str, item: UpdateItemModel) -> PersonalItem | SharedItem:
        try:
            itemDB = self._sess.query(Item).filter(Item.id == item_id).first()
            if not itemDB:
                raise Exception("Item not found")
            for key, value in item.model_dump(exclude_none=True).items():
                setattr(itemDB, key, value)
            self._sess.commit()
            self._sess.refresh(itemDB)
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return itemDB
    
    async def delete(self, item_id: str) -> None:
        try:
            itemDB = self._sess.query(Item).filter(Item.id == item_id).first()
            if not itemDB:
                raise Exception("Item not found")
            self._sess.delete(itemDB)
            self._sess.commit()
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return None

    async def get(self, item_id: str) -> PersonalItem | SharedItem:
        try:
            item = self._sess.query(Item).filter(Item.id == item_id).first()
        except Exception as e:
            raise Exception(e)
        return item