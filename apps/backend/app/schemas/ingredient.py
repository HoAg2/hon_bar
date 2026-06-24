import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.ingredient import IngredientCategory


class IngredientBase(BaseModel):
    name: str
    category: IngredientCategory
    quantity: float = 0.0
    unit: str
    is_available: bool = True
    memo: Optional[str] = None


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[IngredientCategory] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    is_available: Optional[bool] = None
    memo: Optional[str] = None


class IngredientResponse(IngredientBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
