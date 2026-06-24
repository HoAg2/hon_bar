import uuid
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class StockStatus(str, enum.Enum):
    available = "available"
    low = "low"
    empty = "empty"
    unknown = "unknown"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    item_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("item_types.id"), nullable=False)
    stock_status: Mapped[StockStatus] = mapped_column(SAEnum(StockStatus), default=StockStatus.available)
    abv: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    memo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    item_type: Mapped["ItemType"] = relationship(back_populates="items", lazy="selectin")
    tags: Mapped[List["ItemTag"]] = relationship(back_populates="item", cascade="all, delete-orphan", lazy="selectin")
    cocktail_steps: Mapped[List["CocktailStep"]] = relationship(back_populates="item")
    menu_items: Mapped[List["MenuItem"]] = relationship(back_populates="item")
