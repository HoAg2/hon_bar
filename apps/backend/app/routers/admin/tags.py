import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagResponse

router = APIRouter()


@router.get("", response_model=List[TagResponse])
def list_tags(category: str | None = None, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    query = db.query(Tag)
    if category:
        query = query.filter(Tag.category == category)
    return query.all()


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(body: TagCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    tag = Tag(**body.model_dump())
    db.add(tag)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Tag '{body.category}/{body.name}' already exists")
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
