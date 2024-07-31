from fastapi import Depends, HTTPException
from repository.item import ItemRepository
from utils.http import UserSession
from models.item import *
from models.share_item import ShareItemModel
from typing import List


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
            ItemModel(
                id=str(item.id),
                name=item.name,
                site=item.site,
                description=item.description,
                enc_credentials=item.credentials,
                added_at=str(item.added_at),
                type=item.type,
                updated_at=str(item.updated_at) if item.updated_at else None,
                logo_url=item.logo_url if item.logo_url else None
            ).model_dump() 
                if item.type == "personal_item" else 
            ShareItemModel(
                id=str(item.id),
                name=item.name,
                site=item.site,
                description=item.description,
                enc_credentials=item.credentials,
                added_at=str(item.added_at),
                type=item.type,
                updated_at=str(item.updated_at) if item.updated_at else None,
                logo_url=item.logo_url if item.logo_url else None,
                shared_at=str(item.shared_at),
                shared_by=str(item.shared_by),
                enc_pri=item.private_key,
            ).model_dump()
                for item in items
        ]
        return items

    async def create(self, item: CreateItemModel) -> dict[str, str]:
        try:
            item = await self._repo.add(item, str(self._user.id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return ItemModel(
            id=str(item.id),
            name=item.name,
            site=item.site,
            description=item.description,
            enc_credentials=item.credentials,
            added_at=str(item.added_at),
            type=item.type,
            updated_at=str(item.updated_at) if item.updated_at else None,
            logo_url=item.logo_url if item.logo_url else None,
        ).model_dump()

    async def update(self, id: str, item: UpdateItemModel) -> dict[str, str]:
        try:
            item = await self._repo.update(id, item)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return ItemModel(
            id=str(item.id),
            name=item.name,
            site=item.site,
            description=item.description,
            enc_credentials=item.credentials,
            added_at=str(item.added_at),
            type=item.type,
            updated_at=str(item.updated_at) if item.updated_at else None,
            logo_url=item.logo_url if item.logo_url else None,
        ).model_dump()
    
    async def delete(self, id: str) -> None:
        try:
            await self._repo.delete(id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return None