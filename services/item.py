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

    async def create(self, item: AddItemModel) -> dict[str, any]:
        item = await self._repo.add(item, self._user.id)
        return ItemModel(
            id=str(item.id),
            name=item.name,
            site=item.site,
            description=item.description,
            credentials=item.credentials,
        ).model_dump()
