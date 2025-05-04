from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.temporary_list import TemporaryList
from app.models.user import User
from app.models.food_compositions import FoodCompositions
from app.schemas.response import ResponseSchema
from app.schemas.temporary_list import TemporaryListCreate, TemporaryListResponse, TemporaryListWithNamaBahanResponse
from app.routes.auth import get_current_user
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

def generate_response(status_message: str, message: str, data=None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.post("/create", response_model=ResponseSchema[TemporaryListResponse])
def create_temporary_item(
    body: TemporaryListCreate = Depends(TemporaryListCreate.as_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    new_item = TemporaryList(
        user_id=current_user.id,  
        composition_id=body.composition_id,
        date=date.today(),
        type=body.type
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    response_data = TemporaryListResponse.from_orm(new_item)

    response = generate_response(
        status_message="success",
        message="Temporary item created",
        data=response_data
    )

    return JSONResponse(content=jsonable_encoder(response))

@router.get("/", response_model=ResponseSchema[list[TemporaryListWithNamaBahanResponse]])
def get_temporary_list_today(
    type: str = Query(..., regex="^(Breakfast|Lunch|Dinner|Snacks/Other|Ingredients)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    results = (
        db.query(
            TemporaryList.id,
            TemporaryList.user_id,
            TemporaryList.composition_id,
            TemporaryList.date,
            TemporaryList.type,
            FoodCompositions.nama_bahan,
            FoodCompositions.energi
        )
        .join(FoodCompositions, TemporaryList.composition_id == FoodCompositions.id)
        .filter(
            TemporaryList.user_id == current_user.id,
            TemporaryList.date == today,
            TemporaryList.type == type
        )
        .all()
    )

    response_data = [
        TemporaryListWithNamaBahanResponse(
            id=item.id,
            user_id=item.user_id,
            composition_id=item.composition_id,
            date=item.date,
            type=item.type,
            nama_bahan=item.nama_bahan,
            energi=item.energi
        )
        for item in results
    ]

    return generate_response(
        status_message="success",
        message=f"List temporary untuk {type} hari ini",
        data=response_data
    )