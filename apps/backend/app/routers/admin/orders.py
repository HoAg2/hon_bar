import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.order import Order, OrderStatus, OrderType
from app.models.cocktail import Cocktail
from app.models.ingredient import Ingredient
from app.schemas.order import (
    OrderResponse,
    OrderDetailResponse,
    OrderStatusUpdate,
    CocktailDetail,
    IngredientDetail,
    StepDetail,
)

router = APIRouter()


@router.get("", response_model=List[OrderResponse])
def list_orders(
    status: Optional[OrderStatus] = None,
    order_type: Optional[OrderType] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if order_type:
        query = query.filter(Order.order_type == order_type)
    return query.order_by(Order.created_at.desc()).all()


@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order_detail(order_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    detail = OrderDetailResponse.model_validate(order)

    if order.order_type == OrderType.cocktail:
        cocktail = db.get(Cocktail, order.item_id)
        if cocktail:
            detail.cocktail = CocktailDetail(
                name=cocktail.name,
                method=cocktail.method.value,
                glass_type=cocktail.glass_type.value,
                garnish=cocktail.garnish,
                ingredients=[
                    IngredientDetail(
                        name=ing.ingredient.name if ing.ingredient else "Unknown",
                        amount=ing.amount,
                        unit=ing.unit,
                        is_required=ing.is_required,
                    )
                    for ing in cocktail.ingredients
                ],
                steps=[
                    StepDetail(order=step.step_order, description=step.description)
                    for step in cocktail.steps
                ],
            )

    return detail


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: uuid.UUID,
    body: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = body.status
    db.commit()
    db.refresh(order)
    return order
