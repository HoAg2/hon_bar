import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.item import StockStatus
from app.schemas.item_type import ItemTypeResponse
from app.schemas.tag import TagResponse


class ItemBase(BaseModel):
    name: str
    item_type_id: uuid.UUID
    stock_status: StockStatus = StockStatus.available
    abv: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    memo: Optional[str] = None


class ItemCreate(ItemBase):
    tag_ids: List[uuid.UUID] = []


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    item_type_id: Optional[uuid.UUID] = None
    stock_status: Optional[StockStatus] = None
    abv: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    memo: Optional[str] = None
    tag_ids: Optional[List[uuid.UUID]] = None


class ItemTagResponse(BaseModel):
    tag: TagResponse

    model_config = {"from_attributes": True}


class ItemResponse(ItemBase):
    id: uuid.UUID
    item_type: ItemTypeResponse
    tags: List[ItemTagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
