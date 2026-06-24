import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.cocktail import Technique, GlassType, AlcoholLevel


class ItemRef(BaseModel):
    id: uuid.UUID
    name: str

    model_config = {"from_attributes": True}


class CocktailStepBase(BaseModel):
    step_order: int
    instruction: str
    item_id: Optional[uuid.UUID] = None
    amount: Optional[float] = None
    unit: Optional[str] = None
    is_required: bool = True


class CocktailStepResponse(CocktailStepBase):
    id: uuid.UUID
    item: Optional[ItemRef] = None

    model_config = {"from_attributes": True}


class CocktailBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    technique: Technique
    glass_type: GlassType
    alcohol_level: AlcoholLevel
    taste_sweetness: int = 3
    taste_sourness: int = 3
    taste_bitterness: int = 3
    taste_body: int = 3
    taste_freshness: int = 3
    is_active: bool = True


class CocktailCreate(CocktailBase):
    steps: List[CocktailStepBase] = []


class CocktailUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    technique: Optional[Technique] = None
    glass_type: Optional[GlassType] = None
    alcohol_level: Optional[AlcoholLevel] = None
    taste_sweetness: Optional[int] = None
    taste_sourness: Optional[int] = None
    taste_bitterness: Optional[int] = None
    taste_body: Optional[int] = None
    taste_freshness: Optional[int] = None
    is_active: Optional[bool] = None
    steps: Optional[List[CocktailStepBase]] = None


class CocktailResponse(CocktailBase):
    id: uuid.UUID
    steps: List[CocktailStepResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RecommendRequest(BaseModel):
    sweetness: Optional[int] = None
    sourness: Optional[int] = None
    bitterness: Optional[int] = None
    alcohol_level: Optional[AlcoholLevel] = None
    base_item_type_id: Optional[uuid.UUID] = None
