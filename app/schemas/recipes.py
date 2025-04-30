from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import Form, UploadFile
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
