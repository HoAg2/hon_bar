import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.order import OrderStatus
from app.schemas.menu_item import MenuItemResponse


class OrderItemCreate(BaseModel):
    menu_item_id: uuid.UUID
    memo: Optional[str] = None


class OrderCreate(BaseModel):
    guest_name: str
    memo: Optional[str] = None
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    menu_item_id: uuid.UUID
    menu_item: MenuItemResponse
    memo: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    guest_name: str
    status: OrderStatus
    memo: Optional[str] = None
    order_items: List[OrderItemResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}
