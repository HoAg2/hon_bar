import uuid
from typing import Optional
from pydantic import BaseModel


class ItemTypeBase(BaseModel):
    name: str
    display_order: int = 0
    is_visible: bool = True
    is_active: bool = True


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeUpdate(BaseModel):
    name: Optional[str] = None
    display_order: Optional[int] = None
    is_visible: Optional[bool] = None
    is_active: Optional[bool] = None


class ItemTypeResponse(ItemTypeBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}
