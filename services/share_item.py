from fastapi import Depends, HTTPException

from repository.user import UserRepository
from repository.item import ItemRepository

from models.user import *
from models.share_item import *
from models.item import *
from utils.http import *

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

    async def process(self, req: ShareRequest) -> dict[str, str]:
        try:
            item = await self._item_repo.get(req.item_id)
            user = await self._user_repo.get(req.recipient)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        if not item or not user:
            raise HTTPException(status_code=400, detail="Item or User not found")
        if user.id == self._user.id:
            raise HTTPException(status_code=400, detail="Cannot share with yourself")
        return ShareResponse(
            type=item.type,
            enc_credentials=item.enc_credentials,
            enc_pri=user.key.enc_pri,
            recipient_pub=user.key.public_key,
        ).model_dump()
    
    async def create(self, item: CreateShareItem) -> None:
        try:
            recipient = await self._user_repo.get(item.recipient)
            if not recipient:
                raise HTTPException(status_code=400, detail="User not found")
            itemDB = await self._item_repo.get(item.item_id)
            item = AddShareItem(
                name=itemDB.name,
                site=itemDB.site,
                description=itemDB.description,
                enc_credentials=item.enc_credentials,
                enc_pri=recipient.key.enc_pri,
                logo_url=itemDB.logo_url,
            )
            await self._item_repo.add_share(item, str(self._user.id), str(recipient.id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return None



    
    
