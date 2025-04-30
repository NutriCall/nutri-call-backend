from typing import Optional
from pydantic import BaseModel
from fastapi import Form

class UserBase(BaseModel):
    full_name: str
    username: str
    age: int
    weight: int
    weight_target: int
    height: int
    gender: str
    bmi: float
    image_url: Optional[str] = None
    fa: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @classmethod
    def as_form(
        cls,
        full_name: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        age: int = Form(...),
        weight: int = Form(...),
        weight_target: int = Form(...),
        height: int = Form(...),
        gender: str = Form(...),
        bmi: float = Form(...),
        fa: Optional[str] = Form(None),
    ):
        return cls(
            full_name=full_name,
            username=username,
            password=password,
            age=age,
            weight=weight,
            weight_target=weight_target,
            height=height,
            gender=gender,
            bmi=bmi,fa=fa
            )
    
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[int] = None
    weight_target: Optional[int] = None
    height: Optional[int] = None
    gender: Optional[str] = None
    bmi: Optional[float] = None
    image_url: Optional[str] = None
    fa: Optional[str] = None
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
