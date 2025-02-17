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
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
