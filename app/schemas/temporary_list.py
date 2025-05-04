from pydantic import BaseModel, field_validator
from datetime import date
from fastapi import Form

class TemporaryListBase(BaseModel):
    user_id: int
    composition_id: int
    date: date
    type: str
    
class TemporaryListCreate(BaseModel):
    composition_id: int
    type: str
    
    @classmethod
    def as_form(
        cls,
        composition_id: int = Form(...),
        type: str = Form(...)
    ):
        return cls(composition_id=composition_id, type=type)
    
class TemporaryListWithNamaBahanResponse(BaseModel):
    id: int
    user_id: int
    composition_id: int
    date: date
    type: str
    nama_bahan: str
    energi: float
    
    @field_validator("energi", mode="before")
    @classmethod
    def convert_energi(cls, v):
        if isinstance(v, float):
            return round(v / 1000, 2)
        return v

    class Config:
        orm_mode = True
    
class TemporaryListResponse(TemporaryListBase):
    id: int
    
    class Config:
        from_attributes = True
        orm_mode = True