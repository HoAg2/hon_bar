import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.item import StockStatus
from app.schemas.item_type import ItemTypeResponse


class ItemBase(BaseModel):
    name: str
    item_type_id: uuid.UUID
    stock_status: StockStatus = StockStatus.available
    abv: Optional[float] = None
    memo: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    item_type_id: Optional[uuid.UUID] = None
    stock_status: Optional[StockStatus] = None
    abv: Optional[float] = None
    memo: Optional[str] = None


class ItemResponse(ItemBase):
    id: uuid.UUID
    item_type: ItemTypeResponse
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
