from fastapi import Depends, HTTPException
from repository.item import ItemRepository
from utils.http import UserSession
from models.item import *
from models.share_item import *
from typing import List
from fastapi.encoders import jsonable_encoder
from repository.schemas.item import *

def as_dict(item: PersonalItem | SharedItem) -> dict[str, any]:
    match item.type:
        case "personal_item":
            return jsonable_encoder(ItemModel.model_validate(item, strict=False, from_attributes=True))
        case "shared_item":
            itemDict = jsonable_encoder(ShareItemModel.model_validate(item, strict=False, from_attributes=True))
            itemDict.update({
                "shared_by": {
                    "id": str(item.actor.id),
                    "username": item.actor.username,
                    "email": item.actor.email
                }
            })
            return itemDict
        case _:
            return {}

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
            itemsDB = await self._repo.list(str(self._user.id), site)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        if itemsDB is None:
            return []
        items = [as_dict(item) for item in itemsDB]
        return items

    async def create(self, item: CreateItemModel) -> dict[str, str]:
        try:
            personalItem = PersonalItem(
                **item.model_dump(),
                owner_id=str(self._user.id),
            )
            item = await self._repo.add(personalItem)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return jsonable_encoder(ItemModel.model_validate(item, strict=False, from_attributes=True))

    async def update(self, id: str, item: UpdateItemModel) -> dict[str, str]:
        try:
            item = await self._repo.update(id, item)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return as_dict(item)
    
    async def delete(self, id: str) -> None:
        try:
            await self._repo.delete(id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return None