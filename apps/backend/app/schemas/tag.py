import uuid
from typing import Optional
from pydantic import BaseModel


class TagBase(BaseModel):
    category: str
    name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}
