import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.cocktail import AlcoholLevel, GlassType, CocktailMethod


class IngredientRef(BaseModel):
    id: uuid.UUID
    name: str

    model_config = {"from_attributes": True}


class CocktailIngredientBase(BaseModel):
    ingredient_id: uuid.UUID
    amount: float
    unit: str
    is_required: bool = True


class CocktailIngredientResponse(BaseModel):
    id: uuid.UUID
    ingredient: IngredientRef
    amount: float
    unit: str
    is_required: bool

    model_config = {"from_attributes": True}


class CocktailStepBase(BaseModel):
    step_order: int
    description: str


class CocktailStepResponse(CocktailStepBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}


class CocktailBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    alcohol_level: AlcoholLevel
    abv: Optional[float] = None
    base_spirit: Optional[str] = None
    glass_type: GlassType
    method: CocktailMethod
    sweetness: int = 3
    sourness: int = 3
    bitterness: int = 3
    body: int = 3
    freshness: int = 3
    garnish: Optional[str] = None
    is_active: bool = True


class CocktailCreate(CocktailBase):
    ingredients: List[CocktailIngredientBase] = []
    steps: List[CocktailStepBase] = []


class CocktailUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    alcohol_level: Optional[AlcoholLevel] = None
    abv: Optional[float] = None
    base_spirit: Optional[str] = None
    glass_type: Optional[GlassType] = None
    method: Optional[CocktailMethod] = None
    sweetness: Optional[int] = None
    sourness: Optional[int] = None
    bitterness: Optional[int] = None
    body: Optional[int] = None
    freshness: Optional[int] = None
    garnish: Optional[str] = None
    is_active: Optional[bool] = None
    ingredients: Optional[List[CocktailIngredientBase]] = None
    steps: Optional[List[CocktailStepBase]] = None


class CocktailResponse(CocktailBase):
    id: uuid.UUID
    ingredients: List[CocktailIngredientResponse] = []
    steps: List[CocktailStepResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RecommendRequest(BaseModel):
    sweetness: Optional[int] = None
    sourness: Optional[int] = None
    bitterness: Optional[int] = None
    alcohol_level: Optional[AlcoholLevel] = None
    base_spirit: Optional[str] = None
