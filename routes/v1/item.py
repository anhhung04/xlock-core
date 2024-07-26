from fastapi import APIRouter, Depends, Query
from services.item import ItemService
from models.item import *

from utils.http import *

itemRouter = APIRouter()


@itemRouter.get("/", tags=["Item"], response_model=ListItemsResponseModel)
async def list_items(
    site: str = Query(..., title="Site", description="Site name"),
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        200, "Items listed successfully", {"items": await service.list(site)}
    )


@itemRouter.post("/create", tags=["Item"], response_model=ItemResponseModel)
async def create_item(
    item: ItemModel,
    service: ItemService = Depends(ItemService),
):
    return APIResponse.as_json(
        201, "Item created successfully", {"item": await service.create(item)}
    )
