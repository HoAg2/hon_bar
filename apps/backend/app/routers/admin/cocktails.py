import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_admin
from app.models.cocktail import Cocktail, CocktailIngredient, CocktailStep
from app.models.ingredient import Ingredient
from app.schemas.cocktail import CocktailCreate, CocktailUpdate, CocktailResponse

router = APIRouter()


@router.get("", response_model=List[CocktailResponse])
def list_cocktails(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return db.query(Cocktail).all()


@router.post("", response_model=CocktailResponse, status_code=status.HTTP_201_CREATED)
def create_cocktail(body: CocktailCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cocktail = Cocktail(**body.model_dump(exclude={"ingredients", "steps"}))
    db.add(cocktail)
    db.flush()

    for ing in body.ingredients:
        if not db.get(Ingredient, ing.ingredient_id):
            raise HTTPException(status_code=404, detail=f"Ingredient {ing.ingredient_id} not found")
        db.add(CocktailIngredient(cocktail_id=cocktail.id, **ing.model_dump()))

    for step in body.steps:
        db.add(CocktailStep(cocktail_id=cocktail.id, **step.model_dump()))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Cocktail '{body.name}' already exists")
    db.refresh(cocktail)
    return cocktail


@router.get("/{cocktail_id}", response_model=CocktailResponse)
def get_cocktail(cocktail_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cocktail = db.get(Cocktail, cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    return cocktail


@router.put("/{cocktail_id}", response_model=CocktailResponse)
def update_cocktail(cocktail_id: uuid.UUID, body: CocktailUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cocktail = db.get(Cocktail, cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    for key, value in body.model_dump(exclude_none=True, exclude={"ingredients", "steps"}).items():
        setattr(cocktail, key, value)

    if body.ingredients is not None:
        for ci in list(cocktail.ingredients):
            db.delete(ci)
        db.flush()
        for ing in body.ingredients:
            db.add(CocktailIngredient(cocktail_id=cocktail.id, **ing.model_dump()))

    if body.steps is not None:
        for step in list(cocktail.steps):
            db.delete(step)
        db.flush()
        for step in body.steps:
            db.add(CocktailStep(cocktail_id=cocktail.id, **step.model_dump()))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Cocktail name already exists")
    db.refresh(cocktail)
    return cocktail


@router.delete("/{cocktail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cocktail(cocktail_id: uuid.UUID, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cocktail = db.get(Cocktail, cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    db.delete(cocktail)
    db.commit()
