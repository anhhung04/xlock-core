from fastapi import APIRouter, Depends, Query
from services.item import ItemService
from models.item import *

from utils.http import *

itemRouter = APIRouter()


@itemRouter.get("/", tags=["Item"], response_model=ItemListResponse)
async def list_items(
    site: str = Query(..., title="Site", description="Site name"),
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        200, "Items listed successfully", {"items": await service.list(site)}
    )


@itemRouter.post("/create", tags=["Item"], response_model=ItemDetailResponse)
async def create_item(
    item: CreateItemModel,
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        201, "Item created successfully", {"item": await service.create(item)}
    )

@itemRouter.patch("/update/{item_id}", tags=["Item"], response_model=ItemDetailResponse)
async def update_item(
    item_id: str,
    item: UpdateItemModel,
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        201, "Item updated successfully", {"item": await service.update(item_id, item)}
    )

@itemRouter.delete("/delete/{item_id}", tags=["Item"], response_model=DeleteItemResponse)
async def delete_item(
    item_id: str,
    service: ItemService = Depends(ItemService),
):
    await service.delete(item_id)
    return APIResponse.as_json(201, "Item deleted successfully")