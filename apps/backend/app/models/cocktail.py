import uuid
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, DateTime, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class AlcoholLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class GlassType(str, enum.Enum):
    highball = "highball"
    coupe = "coupe"
    rocks = "rocks"
    martini = "martini"
    shot = "shot"
    wine = "wine"
    etc = "etc"


class CocktailMethod(str, enum.Enum):
    build = "build"
    shake = "shake"
    stir = "stir"
    blend = "blend"


class Cocktail(Base):
    __tablename__ = "cocktails"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    alcohol_level: Mapped[AlcoholLevel] = mapped_column(SAEnum(AlcoholLevel), nullable=False)
    abv: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    base_spirit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    glass_type: Mapped[GlassType] = mapped_column(SAEnum(GlassType), nullable=False)
    method: Mapped[CocktailMethod] = mapped_column(SAEnum(CocktailMethod), nullable=False)
    sweetness: Mapped[int] = mapped_column(Integer, default=3)
    sourness: Mapped[int] = mapped_column(Integer, default=3)
    bitterness: Mapped[int] = mapped_column(Integer, default=3)
    body: Mapped[int] = mapped_column(Integer, default=3)
    freshness: Mapped[int] = mapped_column(Integer, default=3)
    garnish: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients: Mapped[List["CocktailIngredient"]] = relationship(
        back_populates="cocktail",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    steps: Mapped[List["CocktailStep"]] = relationship(
        back_populates="cocktail",
        cascade="all, delete-orphan",
        order_by="CocktailStep.step_order",
        lazy="selectin",
    )


class CocktailIngredient(Base):
    __tablename__ = "cocktail_ingredients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cocktail_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cocktails.id", ondelete="CASCADE"), nullable=False)
    ingredient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ingredients.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)

    cocktail: Mapped["Cocktail"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="cocktail_ingredients", lazy="selectin")


class CocktailStep(Base):
    __tablename__ = "cocktail_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cocktail_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cocktails.id", ondelete="CASCADE"), nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    cocktail: Mapped["Cocktail"] = relationship(back_populates="steps")
