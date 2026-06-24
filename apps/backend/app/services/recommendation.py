from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.cocktail import Cocktail, AlcoholLevel
from app.services.availability import get_available_cocktails


def _score(
    cocktail: Cocktail,
    sweetness: Optional[int],
    sourness: Optional[int],
    bitterness: Optional[int],
    alcohol_level: Optional[AlcoholLevel],
    base_spirit: Optional[str],
) -> float:
    score = 0.0

    if sweetness is not None:
        score -= abs(cocktail.sweetness - sweetness)
    if sourness is not None:
        score -= abs(cocktail.sourness - sourness)
    if bitterness is not None:
        score -= abs(cocktail.bitterness - bitterness)
    if alcohol_level and cocktail.alcohol_level == alcohol_level:
        score += 5
    if base_spirit and cocktail.base_spirit and cocktail.base_spirit.lower() == base_spirit.lower():
        score += 5

    return score


def recommend_cocktails(
    db: Session,
    cocktails: List[Cocktail],
    sweetness: Optional[int] = None,
    sourness: Optional[int] = None,
    bitterness: Optional[int] = None,
    alcohol_level: Optional[AlcoholLevel] = None,
    base_spirit: Optional[str] = None,
) -> List[Cocktail]:
    available = get_available_cocktails(db, cocktails)
    scored = [(c, _score(c, sweetness, sourness, bitterness, alcohol_level, base_spirit)) for c in available]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _ in scored]
