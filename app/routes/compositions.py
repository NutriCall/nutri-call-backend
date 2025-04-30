from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.food_compositions import FoodCompositions
from app.schemas.compositions import CompositionResponse, CompositionSearch, CompositionMinimalResponse
from app.routes.auth import get_current_user
from app.schemas.response import ResponseSchema

router = APIRouter()

def generate_response(status_message: str, message: str, data: dict = None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.get("/", response_model=ResponseSchema[List[CompositionResponse]])
def get_all_compositions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    compositions = db.query(FoodCompositions).all()
    return generate_response(
        status_message="success",
        message="Data Found",
        data=compositions
    )

@router.get("/search", response_model=ResponseSchema[List[CompositionMinimalResponse]])
def search_compositions(
    query: CompositionSearch = Depends(), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    compositions = db.query(FoodCompositions).filter(
        FoodCompositions.nama_bahan.ilike(f"%{query.nama_bahan}%")
    ).limit(5).all()  

    if not compositions:
        raise HTTPException(status_code=404, detail="No compositions found")
    
    return generate_response(
        status_message="success",
        message="Compositions found",
        data=compositions
    )

