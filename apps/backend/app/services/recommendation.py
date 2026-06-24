import uuid
from typing import List, Optional
from app.models.cocktail import Cocktail, AlcoholLevel
from app.services.availability import get_available_cocktails


def _score(
    cocktail: Cocktail,
    sweetness: Optional[int],
    sourness: Optional[int],
    bitterness: Optional[int],
    alcohol_level: Optional[AlcoholLevel],
    base_item_type_id: Optional[uuid.UUID],
) -> float:
    score = 0.0

    if sweetness is not None:
        score -= abs(cocktail.taste_sweetness - sweetness)
    if sourness is not None:
        score -= abs(cocktail.taste_sourness - sourness)
    if bitterness is not None:
        score -= abs(cocktail.taste_bitterness - bitterness)
    if alcohol_level and cocktail.alcohol_level == alcohol_level:
        score += 5
    if base_item_type_id:
        for step in cocktail.steps:
            if step.item and step.item.item_type_id == base_item_type_id:
                score += 5
                break

    return score


def recommend_cocktails(
    cocktails: List[Cocktail],
    sweetness: Optional[int] = None,
    sourness: Optional[int] = None,
    bitterness: Optional[int] = None,
    alcohol_level: Optional[AlcoholLevel] = None,
    base_item_type_id: Optional[uuid.UUID] = None,
) -> List[Cocktail]:
    available = get_available_cocktails(cocktails)
    scored = [(c, _score(c, sweetness, sourness, bitterness, alcohol_level, base_item_type_id)) for c in available]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _ in scored]
