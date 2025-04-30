from pydantic import BaseModel
from datetime import date
from typing import List

class MealsBase(BaseModel):
    user_id: int
    composition_id: int
    date: date
    type: str

class MealsCreate(BaseModel):
    compositions: List[int]
    type: str

class MealsResponse(MealsBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
        
class FoodCompositionDetails(BaseModel):
    nama_bahan: str
    energi: float
    karbohidrat: float
    protein: float
    lemak: float

    class Config:
        orm_mode = True

class MealsWithDetailsResponse(BaseModel):
    id: int
    user_id: int
    composition_id: int
    date: date
    type: str
    food_composition: FoodCompositionDetails

class MealsWithTotalEnergyResponse(BaseModel):
    type: str
    meals: list[MealsWithDetailsResponse]
    total_energi: float

    class Config:
        orm_mode = True
