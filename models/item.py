from pydantic import BaseModel


class AddItemModel(BaseModel):
    name: str
    site: str
    description: str
    credentials: str

class ItemModel(AddItemModel):
    id: str

class ListItemsResponseModel(BaseModel):
    items: list[ItemModel]


class ItemResponseModel(BaseModel):
    item: ItemModel
