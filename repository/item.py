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

    async def list(self, id: str, site: str | None) -> List[PersonalItem | SharedItem]: 
        try:
            items = self._sess.query(Item).filter(Item.owner_id == id)
            items = items.filter(Item.site == site).all() if site else items.all()
        except Exception as e:
            raise Exception(e)
        return items

    async def add(self, item: CreateItemModel, user_id: str) -> PersonalItem:
        try:
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
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return personalItem
    
    async def update(self, item_id: str, item: UpdateItemModel) -> PersonalItem:
        try:
            personalItem = self._sess.query(PersonalItem).filter(PersonalItem.id == item_id).first()
            if not personalItem:
                raise Exception("Item not found")
            for key, value in item.model_dump(exclude_none=True).items():
                setattr(personalItem, key, value)
            self._sess.commit()
            self._sess.refresh(personalItem)
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return personalItem
    
    async def delete(self, item_id: str) -> None:
        try:
            personalItem = self._sess.query(PersonalItem).filter(PersonalItem.id == item_id).first()
            if not personalItem:
                raise Exception("Item not found")
            self._sess.delete(personalItem)
            self._sess.commit()
        except Exception as e:
            self._sess.rollback()
            raise Exception(e)
        return None
