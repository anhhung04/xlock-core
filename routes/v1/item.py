from fastapi import APIRouter, Depends, Query
from services.item import ItemService
from services.share_item import ShareService
from typing import Optional
from models.share_item import *
from models.item import *
from utils.http import *

itemRouter = APIRouter()


@itemRouter.get("/", tags=["Item"], response_model=ItemListResponse)
async def list_items(
    site: Optional[str] = Query(None, title="Site", description="Site name"),
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        200, "Items listed successfully", await service.list(site)
    )


@itemRouter.post("/create", tags=["Item"], response_model=ItemDetailResponse)
async def create_item(
    item: CreateItemModel,
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        201, "Item created successfully", await service.create(item)
    )

@itemRouter.patch("/update/{item_id}", tags=["Item"], response_model=ItemDetailResponse)
async def update_item(
    item_id: str,
    item: UpdateItemModel,
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        200, "Item updated successfully", await service.update(item_id, item)
    )

@itemRouter.delete("/delete/{item_id}", tags=["Item"], response_model=DeleteItemResponse)
async def delete_item(
    item_id: str,
    service: ItemService = Depends(ItemService),
):
    await service.delete(item_id)
    return APIResponse.as_json(
        201, "Item deleted successfully", None
    )

@itemRouter.post("/share", tags=["Item"], response_model=ShareResponseModel)
async def share_item(
    share_req: ShareRequest,
    service: ShareService = Depends(ShareService),
):
    return APIResponse.as_json(
        200, "OK", await service.process(share_req)
    )

@itemRouter.post("/share/create", tags=["Item"], response_model=BaseResponseModel)
async def create_shared_item(
    item: CreateShareItem,
    service: ShareService = Depends(ShareService),
):
    await service.create(item)
    return APIResponse.as_json(
        201, "Shared item created successfully", None
    )