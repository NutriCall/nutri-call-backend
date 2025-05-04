from pydantic import BaseModel, field_validator
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
        
    @field_validator('*', mode='before')
    @classmethod
    def round_floats(cls, v, info):
        if isinstance(v, float):
            if info.field_name == 'energi':
                return round(v / 1000, 2)
            return round(v, 2)
        return v

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
    
    @field_validator('total_energi', mode='before')
    @classmethod
    def round_total_energy(cls, v):
        if isinstance(v, float):
            return round(v / 1000, 2)
        return v

    class Config:
        orm_mode = True
