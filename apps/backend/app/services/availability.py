from typing import List
from app.models.cocktail import Cocktail
from app.models.item import StockStatus


def is_cocktail_available(cocktail: Cocktail) -> bool:
    for step in cocktail.steps:
        if step.is_required and step.item_id is not None:
            if step.item is None or step.item.stock_status == StockStatus.empty:
                return False
    return True


def get_available_cocktails(cocktails: List[Cocktail]) -> List[Cocktail]:
    return [c for c in cocktails if c.is_active and is_cocktail_available(c)]
