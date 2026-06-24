import uuid
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class IngredientCategory(str, enum.Enum):
    base_spirit = "base_spirit"
    liqueur = "liqueur"
    juice = "juice"
    soda = "soda"
    syrup = "syrup"
    fruit = "fruit"
    garnish = "garnish"
    bitter = "bitter"
    dairy = "dairy"
    etc = "etc"


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[IngredientCategory] = mapped_column(SAEnum(IngredientCategory), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, default=0.0)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    memo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cocktail_ingredients: Mapped[List["CocktailIngredient"]] = relationship(back_populates="ingredient")
