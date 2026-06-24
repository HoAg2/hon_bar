import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator
from app.schemas.cocktail import CocktailResponse
from app.schemas.item import ItemResponse


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    cocktail_id: Optional[uuid.UUID] = None
    item_id: Optional[uuid.UUID] = None
    is_active: bool = True
    display_order: int = 0

    @model_validator(mode="after")
    def check_exactly_one_target(self):
        if (self.cocktail_id is None) == (self.item_id is None):
            raise ValueError("Exactly one of cocktail_id or item_id must be provided")
        return self


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class MenuItemResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    cocktail_id: Optional[uuid.UUID] = None
    item_id: Optional[uuid.UUID] = None
    is_active: bool
    display_order: int
    cocktail: Optional[CocktailResponse] = None
    item: Optional[ItemResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
