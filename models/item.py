from pydantic import BaseModel


class ItemModel(BaseModel):
    id: str
    name: str
    site: str
    description: str
    credentials: str


class ListItemsResponseModel(BaseModel):
    items: list[ItemModel]


class ItemResponseModel(BaseModel):
    item: ItemModel
