from pydantic import BaseModel
from typing import Optional

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
    
class CompositionSearch(BaseModel):
    nama_bahan: Optional[str] = None
    
class CompositionMinimalResponse(BaseModel):
    id: int
    nama_bahan: str

class CompositionResponse(CompositionBase):
    id: int

    class Config:
        from_attributes = True
