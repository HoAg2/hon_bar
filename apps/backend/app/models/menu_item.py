import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    full_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cocktail_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("cocktails.id"), nullable=True)
    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cocktail: Mapped[Optional["Cocktail"]] = relationship(back_populates="menu_items", lazy="selectin")
    item: Mapped[Optional["Item"]] = relationship(back_populates="menu_items", lazy="selectin")
    tags: Mapped[List["MenuItemTag"]] = relationship(back_populates="menu_item", cascade="all, delete-orphan", lazy="selectin")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="menu_item")
    reviews: Mapped[List["Review"]] = relationship(back_populates="menu_item")


class MenuItemTag(Base):
    __tablename__ = "menu_item_tags"

    menu_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("menu_items.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    menu_item: Mapped["MenuItem"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="menu_item_tags", lazy="selectin")
