import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.item_type import ItemType
from app.schemas.item_type import ItemTypeCreate, ItemTypeUpdate, ItemTypeResponse

router = APIRouter()


@router.get("", response_model=List[ItemTypeResponse])
def list_item_types(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(ItemType).order_by(ItemType.display_order).all()


@router.post("", response_model=ItemTypeResponse, status_code=status.HTTP_201_CREATED)
def create_item_type(body: ItemTypeCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item_type = ItemType(**body.model_dump())
    db.add(item_type)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"ItemType '{body.name}' already exists")
    db.refresh(item_type)
    return item_type


@router.put("/{type_id}", response_model=ItemTypeResponse)
def update_item_type(type_id: uuid.UUID, body: ItemTypeUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item_type = db.get(ItemType, type_id)
    if not item_type:
        raise HTTPException(status_code=404, detail="ItemType not found")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(item_type, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ItemType name already exists")
    db.refresh(item_type)
    return item_type


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_type(type_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item_type = db.get(ItemType, type_id)
    if not item_type:
        raise HTTPException(status_code=404, detail="ItemType not found")
    db.delete(item_type)
    db.commit()
