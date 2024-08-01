from fastapi import Depends, HTTPException
from repository.item import ItemRepository
from utils.http import UserSession
from models.item import *
from models.share_item import ShareItemModel
from typing import List
from fastapi.encoders import jsonable_encoder


class ItemService:

    def __init__(
        self,
        repo: ItemRepository = Depends(ItemRepository),
        session: UserSession = Depends(UserSession),
    ):
        self._repo = repo
        self._user = session._user

    async def list(self, site: str | None) -> List[dict[str, any]]:
        try:
            items = await self._repo.list(str(self._user.id), site)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        if items is None:
            return []
        items = [
            jsonable_encoder(ItemModel.model_validate(item, strict=False, from_attributes=True))
                if item.type == "personal_item" else 
            jsonable_encoder(ShareItemModel.model_validate(item, strict=False, from_attributes=True))
                for item in items
        ]
        return items

    async def create(self, item: CreateItemModel) -> dict[str, str]:
        try:
            item = await self._repo.add(item, str(self._user.id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return jsonable_encoder(ItemModel.model_validate(item, strict=False, from_attributes=True))

    async def update(self, id: str, item: UpdateItemModel) -> dict[str, str]:
        try:
            item = await self._repo.update(id, item)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        if item.type == "personal_item":
            return jsonable_encoder(ItemModel.model_validate(item, strict=False, from_attributes=True))
        else:
            return jsonable_encoder(ShareItemModel.model_validate(item, strict=False, from_attributes=True))
    
    async def delete(self, id: str) -> None:
        try:
            await self._repo.delete(id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return None