from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.food_compositions import FoodCompositions
from app.schemas.compositions import CompositionResponse, CompositionSearch, CompositionMinimalResponse, NutrientCalculationRequest, NutrientResult
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

@router.post("/calculate-nutrients", response_model=ResponseSchema[CompositionResponse])
def calculate_nutrients(
    request: NutrientCalculationRequest = Depends(NutrientCalculationRequest.as_form),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    bahan = db.query(FoodCompositions).filter(
        FoodCompositions.nama_bahan.ilike(f"%{request.nama_bahan}%")
    ).first()

    if not bahan:
        raise HTTPException(status_code=404, detail="Bahan tidak ditemukan")

    faktor = request.size / 100.0

    new_composition = FoodCompositions(
        kode=None,
        nama_bahan=bahan.nama_bahan,
        sumber=bahan.sumber,
        air=(bahan.air or 0) * faktor,
        energi=(bahan.energi or 0) * faktor,
        protein=(bahan.protein or 0) * faktor,
        lemak=(bahan.lemak or 0) * faktor,
        karbohidrat=(bahan.karbohidrat or 0) * faktor,
        serat=(bahan.serat or 0) * faktor,
        abu=(bahan.abu or 0) * faktor,
        kalsium=(bahan.kalsium or 0) * faktor,
        fosfor=(bahan.fosfor or 0) * faktor,
        besi=(bahan.besi or 0) * faktor,
        natrium=(bahan.natrium or 0) * faktor,
        kalium=(bahan.kalium or 0) * faktor,
        tembaga=(bahan.tembaga or 0) * faktor,
        seng=(bahan.seng or 0) * faktor,
        retinol=(bahan.retinol or 0) * faktor,
        beta_karoten=(bahan.beta_karoten or 0) * faktor,
        karoten_total=(bahan.karoten_total or 0) * faktor,
        tiamin=(bahan.tiamin or 0) * faktor,
        riboflavin=(bahan.riboflavin or 0) * faktor,
        niasin=(bahan.niasin or 0) * faktor,
        vit_c=(bahan.vit_c or 0) * faktor,
        bdd=bahan.bdd,
        size=request.size
    )

    db.add(new_composition)
    db.commit()
    db.refresh(new_composition)

    return generate_response(
        status_message="success",
        message="Perhitungan dan penyimpanan gizi berhasil",
        data=new_composition
    )

