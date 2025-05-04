from pydantic import BaseModel, field_validator
from typing import List, Optional
from fastapi import Form
from datetime import date

class StepCreate(BaseModel):
    step: str

class IngredientCreate(BaseModel):
    composition_id: int

class RecipeBase(BaseModel):
    name: str
    title: str
    sumber: Optional[str] = None

class RecipeCreate(BaseModel):
    name: str
    title: str
    sumber: Optional[str] = None
    ingredients: List[int]
    steps: List[str]

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        title: str = Form(...),
        sumber: Optional[str] = Form(None),
        ingredients: List[int] = Form(...),
        steps: List[str] = Form(...)
    ):
        return cls(name=name, title=title, sumber=sumber, ingredients=ingredients, steps=steps)

class RecipeResponse(BaseModel):
    id: int
    name: str
    user_id: int
    date: date
    image_url: Optional[str]
    title: str
    sumber: Optional[str]
    energi: Optional[float]
    protein: Optional[float]
    lemak: Optional[float]
    karbohidrat: Optional[float]
    
    @field_validator("*", mode="before")
    @classmethod
    def format_values(cls, v, info):
        if isinstance(v, float):
            if info.field_name == "energi":
                return round(v / 1000, 2)
            return round(v, 2)
        return v

    class Config:
        orm_mode = True

class RecipeListItemSchema(BaseModel):
    id: int
    name: str
    date: date
    image_url: Optional[str]
    user_id: int
    user_full_name: str
    user_image: Optional[str]

    class Config:
        from_attributes = True
