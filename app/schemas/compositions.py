from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import Form

class NutrientCalculationRequest(BaseModel):
    nama_bahan: str
    size: float
    
    @classmethod
    def as_form(
        cls,
        nama_bahan: str = Form(...),
        size: float = Form(...),
    ):
        return cls(
            nama_bahan=nama_bahan,
            size=size
        )
    
class NutrientResult(BaseModel):
    nama_bahan: str
    size: float
    air: Optional[float]
    energi: Optional[float]
    protein: Optional[float]
    lemak: Optional[float]
    karbohidrat: Optional[float]
    serat: Optional[float]
    abu: Optional[float]
    kalsium: Optional[float]
    fosfor: Optional[float]
    besi: Optional[float]
    natrium: Optional[float]
    kalium: Optional[float]
    tembaga: Optional[float]
    seng: Optional[float]
    retinol: Optional[float]
    beta_karoten: Optional[float]
    karoten_total: Optional[float]
    tiamin: Optional[float]
    riboflavin: Optional[float]
    niasin: Optional[float]
    vit_c: Optional[float]
    size: Optional[float]
    
    @field_validator('*', mode='before')
    @classmethod
    def round_and_convert(cls, v, info):
        if isinstance(v, float):
            if info.field_name == 'energi':
                return round(v / 1000, 2)
            return round(v, 2)
        return v

class CompositionBase(BaseModel):
    kode: Optional[str] = None
    nama_bahan: str
    sumber: Optional[str] = None
    air: Optional[float] = None
    energi: Optional[float] = None
    protein: Optional[float] = None
    lemak: Optional[float] = None
    karbohidrat: Optional[float] = None
    serat: Optional[float] = None
    abu: Optional[float] = None
    kalsium: Optional[float] = None
    fosfor: Optional[float] = None
    besi: Optional[float] = None
    natrium: Optional[float] = None
    kalium: Optional[float] = None
    tembaga: Optional[float] = None
    seng: Optional[float] = None
    retinol: Optional[float] = None
    beta_karoten: Optional[float] = None
    karoten_total: Optional[float] = None
    tiamin: Optional[float] = None
    riboflavin: Optional[float] = None
    niasin: Optional[float] = None
    vit_c: Optional[float] = None
    bdd: Optional[float] = None
    size: Optional[float] = None
    
class CompositionSearch(BaseModel):
    nama_bahan: Optional[str] = None
    
class CompositionMinimalResponse(BaseModel):
    id: int
    nama_bahan: str
    energi: float
    
    @field_validator('energi', mode='before')
    @classmethod
    def convert_energi(cls, v):
        return round((v or 0) / 1000, 2)

class CompositionResponse(CompositionBase):
    id: int
    
    @field_validator('*', mode='before')
    @classmethod
    def round_float(cls, v, info):
        if isinstance(v, float):
            field_name = info.field_name
            if field_name == 'energi':
                return round(v / 1000, 2)  
            return round(v, 2)
        return v

    class Config:
        from_attributes = True
