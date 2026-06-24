import uuid
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, DateTime, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Technique(str, enum.Enum):
    build = "build"
    shake = "shake"
    stir = "stir"
    blend = "blend"


class GlassType(str, enum.Enum):
    highball = "highball"
    coupe = "coupe"
    rocks = "rocks"
    martini = "martini"
    shot = "shot"
    wine = "wine"
    etc = "etc"


class AlcoholLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Cocktail(Base):
    __tablename__ = "cocktails"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    technique: Mapped[Technique] = mapped_column(SAEnum(Technique), nullable=False)
    glass_type: Mapped[GlassType] = mapped_column(SAEnum(GlassType), nullable=False)
    alcohol_level: Mapped[AlcoholLevel] = mapped_column(SAEnum(AlcoholLevel), nullable=False)
    taste_sweetness: Mapped[int] = mapped_column(Integer, default=3)
    taste_sourness: Mapped[int] = mapped_column(Integer, default=3)
    taste_bitterness: Mapped[int] = mapped_column(Integer, default=3)
    taste_body: Mapped[int] = mapped_column(Integer, default=3)
    taste_freshness: Mapped[int] = mapped_column(Integer, default=3)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    steps: Mapped[List["CocktailStep"]] = relationship(
        back_populates="cocktail",
        cascade="all, delete-orphan",
        order_by="CocktailStep.step_order",
        lazy="selectin",
    )
    menu_items: Mapped[List["MenuItem"]] = relationship(back_populates="cocktail")


class CocktailStep(Base):
    __tablename__ = "cocktail_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cocktail_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cocktails.id", ondelete="CASCADE"), nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    instruction: Mapped[str] = mapped_column(Text, nullable=False)
    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)

    cocktail: Mapped["Cocktail"] = relationship(back_populates="steps")
    item: Mapped[Optional["Item"]] = relationship(back_populates="cocktail_steps", lazy="selectin")
