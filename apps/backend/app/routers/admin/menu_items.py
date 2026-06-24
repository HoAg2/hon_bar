import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.menu_item import MenuItem, MenuItemTag
from app.models.tag import Tag
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse

router = APIRouter()


@router.get("", response_model=List[MenuItemResponse])
def list_menu_items(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(MenuItem).order_by(MenuItem.display_order).all()


@router.post("", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(body: MenuItemCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    menu_item = MenuItem(**body.model_dump(exclude={"tag_ids"}))
    db.add(menu_item)
    db.flush()
    _sync_tags(db, menu_item, body.tag_ids)
    db.commit()
    db.refresh(menu_item)
    return menu_item


@router.get("/{menu_item_id}", response_model=MenuItemResponse)
def get_menu_item(menu_item_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    menu_item = db.get(MenuItem, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="MenuItem not found")
    return menu_item


@router.put("/{menu_item_id}", response_model=MenuItemResponse)
def update_menu_item(menu_item_id: uuid.UUID, body: MenuItemUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    menu_item = db.get(MenuItem, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="MenuItem not found")
    for key, value in body.model_dump(exclude_none=True, exclude={"tag_ids"}).items():
        setattr(menu_item, key, value)
    if body.tag_ids is not None:
        for mt in list(menu_item.tags):
            db.delete(mt)
        db.flush()
        _sync_tags(db, menu_item, body.tag_ids)
    db.commit()
    db.refresh(menu_item)
    return menu_item


@router.delete("/{menu_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(menu_item_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    menu_item = db.get(MenuItem, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="MenuItem not found")
    db.delete(menu_item)
    db.commit()


def _sync_tags(db: Session, menu_item: MenuItem, tag_ids: List[uuid.UUID]):
    for tag_id in tag_ids:
        if not db.get(Tag, tag_id):
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        db.add(MenuItemTag(menu_item_id=menu_item.id, tag_id=tag_id))
