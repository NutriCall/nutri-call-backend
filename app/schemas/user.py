from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    full_name: str
    username: str
    age: int
    weight: int
    weight_target: int
    height: int
    gender: str
    bmi: float

class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[int] = None
    weight_target: Optional[int] = None
    height: Optional[int] = None
    gender: Optional[str] = None
    bmi: Optional[float] = None
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
