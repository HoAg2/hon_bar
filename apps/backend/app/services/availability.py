from typing import List
from sqlalchemy.orm import Session
from app.models.cocktail import Cocktail
from app.models.ingredient import Ingredient


def is_cocktail_available(db: Session, cocktail: Cocktail) -> bool:
    for ci in cocktail.ingredients:
        if not ci.is_required:
            continue
        ingredient = db.get(Ingredient, ci.ingredient_id)
        if not ingredient or not ingredient.is_available:
            return False
    return True


def get_available_cocktails(db: Session, cocktails: List[Cocktail]) -> List[Cocktail]:
    return [c for c in cocktails if c.is_active and is_cocktail_available(db, c)]
