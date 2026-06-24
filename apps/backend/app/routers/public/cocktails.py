import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cocktail import Cocktail
from app.models.order import Order, OrderType
from app.schemas.cocktail import CocktailResponse, RecommendRequest
from app.schemas.order import OrderCreate, OrderResponse
from app.services.availability import get_available_cocktails
from app.services.recommendation import recommend_cocktails

router = APIRouter()


@router.get("/available", response_model=List[CocktailResponse])
def list_available_cocktails(db: Session = Depends(get_db)):
    cocktails = db.query(Cocktail).filter(Cocktail.is_active == True).all()
    return get_available_cocktails(db, cocktails)


@router.post("/recommend", response_model=List[CocktailResponse])
def recommend(body: RecommendRequest, db: Session = Depends(get_db)):
    cocktails = db.query(Cocktail).filter(Cocktail.is_active == True).all()
    return recommend_cocktails(
        db,
        cocktails,
        sweetness=body.sweetness,
        sourness=body.sourness,
        bitterness=body.bitterness,
        alcohol_level=body.alcohol_level,
        base_spirit=body.base_spirit,
    )


@router.get("/{cocktail_id}", response_model=CocktailResponse)
def get_cocktail(cocktail_id: uuid.UUID, db: Session = Depends(get_db)):
    cocktail = db.get(Cocktail, cocktail_id)
    if not cocktail or not cocktail.is_active:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    return cocktail


@router.post("/{cocktail_id}/order", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(cocktail_id: uuid.UUID, body: OrderCreate, db: Session = Depends(get_db)):
    cocktail = db.get(Cocktail, cocktail_id)
    if not cocktail or not cocktail.is_active:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    order = Order(order_type=OrderType.cocktail, item_id=cocktail_id, **body.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
