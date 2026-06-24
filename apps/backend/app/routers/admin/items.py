import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.item import Item
from app.models.tag import Tag, ItemTag
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
    item = Item(**body.model_dump(exclude={"tag_ids"}))
    db.add(item)
    db.flush()
    _sync_tags(db, item, body.tag_ids)
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
    for key, value in body.model_dump(exclude_none=True, exclude={"tag_ids"}).items():
        setattr(item, key, value)
    if body.tag_ids is not None:
        for it in list(item.tags):
            db.delete(it)
        db.flush()
        _sync_tags(db, item, body.tag_ids)
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


def _sync_tags(db: Session, item: Item, tag_ids: List[uuid.UUID]):
    for tag_id in tag_ids:
        if not db.get(Tag, tag_id):
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        db.add(ItemTag(item_id=item.id, tag_id=tag_id))
