import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.order import OrderType, OrderStatus


class OrderCreate(BaseModel):
    guest_name: str
    memo: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: uuid.UUID
    order_type: OrderType
    item_id: uuid.UUID
    guest_name: str
    status: OrderStatus
    memo: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class IngredientDetail(BaseModel):
    name: str
    amount: float
    unit: str
    is_required: bool


class StepDetail(BaseModel):
    order: int
    description: str


class CocktailDetail(BaseModel):
    name: str
    method: str
    glass_type: str
    garnish: Optional[str] = None
    ingredients: List[IngredientDetail] = []
    steps: List[StepDetail] = []


class OrderDetailResponse(OrderResponse):
    cocktail: Optional[CocktailDetail] = None
