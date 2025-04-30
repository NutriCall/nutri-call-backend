from pydantic import BaseModel
from typing import Optional
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

    class Config:
        orm_mode = True
    
class TemporaryListResponse(TemporaryListBase):
    id: int
    
    class Config:
        from_attributes = True
        orm_mode = True