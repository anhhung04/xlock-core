from fastapi import Depends
from repository.item import ItemRepository
from utils.http import UserSession
from models.item import *
from typing import List


class ItemService:

    def __init__(
        self,
        repo: ItemRepository = Depends(ItemRepository),
        session: UserSession = Depends(UserSession),
    ):
        self._repo = repo
        self._user = session._user

    async def list(self, site: str) -> List[dict[str, any]]:
        items = await self._repo.list(site)
        items = [
            ItemModel.model_validate(
                item, from_attributes=True, strict=False
            ).model_dump()
            for item in items
        ]
        return items

    async def create(self, item: ItemModel) -> dict[str, any]:
        item = ItemModel.model_validate(
            await self._repo.add(item, self._user), strict=False, from_attributes=True
        )

        return item.model_dump()
