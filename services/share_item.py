from fastapi import Depends, HTTPException

from repository.user import UserRepository
from repository.item import ItemRepository, SharedItem

from models.user import *
from models.share_item import *
from models.item import *

from utils.http import *
from utils.session import *


class ShareService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        item_repo: ItemRepository = Depends(ItemRepository),
        user: UserSession = Depends(UserSession),
    ):
        self._user_repo = user_repo
        self._item_repo = item_repo
        self._user = user._user

    async def create(self, item: CreateShareItem) -> None:
        try:
            recipient = await self._user_repo.get(
                QueryUserModel(**item.validate_recipient())
            )
            if not recipient:
                raise HTTPException(status_code=400, detail="User not found")
            itemDB = await self._item_repo.get(item.item_id)
            if not itemDB:
                raise HTTPException(status_code=400, detail="Item not found")
            sharedItem = SharedItem(
                name=itemDB.name,
                site=itemDB.site,
                description=itemDB.description,
                enc_credentials=item.enc_credentials,
                enc_pri=recipient.key.enc_pri,
                logo_url=itemDB.logo_url,
                owner_id=str(recipient.id),
                actor_id=str(self._user.id),
            )
            await self._item_repo.add(sharedItem)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return None
