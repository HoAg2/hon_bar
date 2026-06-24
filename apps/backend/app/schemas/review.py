import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    menu_item_id: uuid.UUID
    guest_name: str
    rating: int = Field(ge=1, le=5)
    content: Optional[str] = None


class ReviewResponse(BaseModel):
    id: uuid.UUID
    menu_item_id: uuid.UUID
    guest_name: str
    rating: int
    content: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
