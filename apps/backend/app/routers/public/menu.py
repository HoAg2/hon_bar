import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cocktail import Cocktail
from app.models.menu_item import MenuItem, MenuItemTag
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.tag import Tag
from app.schemas.cocktail import RecommendRequest, CocktailResponse
from app.schemas.menu_item import MenuItemResponse
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.review import ReviewCreate, ReviewResponse
from app.schemas.tag import TagResponse
from app.services.availability import get_available_cocktails
from app.services.recommendation import recommend_cocktails

router = APIRouter()


@router.get("/tags", response_model=List[TagResponse])
def list_tags(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Tag)
    if category:
        query = query.filter(Tag.category == category)
    return query.all()


@router.get("/cocktails/available", response_model=List[CocktailResponse])
def list_available_cocktails(db: Session = Depends(get_db)):
    cocktails = db.query(Cocktail).filter(Cocktail.is_active == True).all()
    return get_available_cocktails(cocktails)


@router.post("/cocktails/recommend", response_model=List[CocktailResponse])
def recommend(body: RecommendRequest, db: Session = Depends(get_db)):
    cocktails = db.query(Cocktail).filter(Cocktail.is_active == True).all()
    return recommend_cocktails(
        cocktails,
        sweetness=body.sweetness,
        sourness=body.sourness,
        bitterness=body.bitterness,
        alcohol_level=body.alcohol_level,
        base_item_type_id=body.base_item_type_id,
    )


@router.get("/menu", response_model=List[MenuItemResponse])
def list_menu(
    tag_id: Optional[uuid.UUID] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(MenuItem).filter(MenuItem.is_active == True)
    if tag_id:
        query = query.filter(MenuItem.tags.any(MenuItemTag.tag_id == tag_id))
    if search:
        query = query.filter(
            MenuItem.display_name.ilike(f"%{search}%") |
            MenuItem.short_description.ilike(f"%{search}%")
        )
    return query.order_by(MenuItem.display_order).all()


@router.get("/menu/{menu_item_id}", response_model=MenuItemResponse)
def get_menu_item(menu_item_id: uuid.UUID, db: Session = Depends(get_db)):
    menu_item = db.get(MenuItem, menu_item_id)
    if not menu_item or not menu_item.is_active:
        raise HTTPException(status_code=404, detail="MenuItem not found")
    return menu_item


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    order = Order(guest_name=body.guest_name, memo=body.memo)
    db.add(order)
    db.flush()
    for oi in body.items:
        menu_item = db.get(MenuItem, oi.menu_item_id)
        if not menu_item or not menu_item.is_active:
            raise HTTPException(status_code=404, detail=f"MenuItem {oi.menu_item_id} not found")
        db.add(OrderItem(order_id=order.id, menu_item_id=oi.menu_item_id, memo=oi.memo))
    db.commit()
    db.refresh(order)
    return order


@router.get("/reviews", response_model=List[ReviewResponse])
def list_reviews(menu_item_id: Optional[uuid.UUID] = None, db: Session = Depends(get_db)):
    query = db.query(Review)
    if menu_item_id:
        query = query.filter(Review.menu_item_id == menu_item_id)
    return query.order_by(Review.created_at.desc()).all()


@router.post("/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(body: ReviewCreate, db: Session = Depends(get_db)):
    if not db.get(MenuItem, body.menu_item_id):
        raise HTTPException(status_code=404, detail="MenuItem not found")
    review = Review(**body.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
