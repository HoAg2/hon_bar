import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.get("", response_model=List[ItemResponse])
def list_items(item_type_id: uuid.UUID | None = None, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    query = db.query(Item)
    if item_type_id:
        query = query.filter(Item.item_type_id == item_type_id)
    return query.all()


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(body: ItemCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item = Item(**body.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Item '{body.name}' already exists")
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: uuid.UUID, body: ItemUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(item, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item name already exists")
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
