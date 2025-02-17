import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.response import ResponseSchema
from app.utils.security import get_current_user, hash_password, verify_password, create_access_token
from fastapi.responses import FileResponse
from app.config import APP_URL 

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def generate_response(status_message: str, message: str, data: dict = None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.post("/signup", response_model=ResponseSchema[UserResponse])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        full_name=user.full_name,
        username=user.username,
        password_hash=hash_password(user.password),
        age=user.age,
        weight=user.weight,
        weight_target=user.weight_target,
        height=user.height,
        gender=user.gender,
        bmi=user.bmi
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_response = UserResponse.model_validate(new_user)
    return generate_response("success", "User registered successfully", user_response)

@router.post("/login", response_model=ResponseSchema[dict])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    
    user_response = UserResponse.model_validate(user)
    return generate_response("success", "Login successful", {
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    })

@router.post("/logout", response_model=ResponseSchema[None])
def logout_user():
    return generate_response("success", "Logout successful. Delete token on client side")

UPLOAD_DIR = "uploads/"  

@router.put("/edit-profile", response_model=ResponseSchema[UserResponse])
def update_user_profile(
    full_name: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    weight: Optional[int] = Form(None),
    weight_target: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    gender: Optional[str] = Form(None),
    bmi: Optional[float] = Form(None),
    image_url: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if full_name:
        current_user.full_name = full_name
    if age:
        current_user.age = age
    if weight:
        current_user.weight = weight
    if weight_target:
        current_user.weight_target = weight_target
    if height:
        current_user.height = height
    if gender:
        current_user.gender = gender
    if bmi:
        current_user.bmi = bmi

    if image_url:
        file_extension = image_url.filename.split(".")[-1]
        filename = f"user_{current_user.id}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_url.file, buffer)

        current_user.image_url = f"/uploads/{filename}" 

    db.commit()
    db.refresh(current_user)

    user_response = UserResponse.model_validate(current_user)
    if user_response.image_url:
        user_response.image_url = f"{APP_URL}{user_response.image_url}"    
    return generate_response("success", "Profile updated successfully", user_response)

@router.get("/user", response_model=ResponseSchema[UserResponse])
def get_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = f"{APP_URL}{current_user.image_url}" if current_user.image_url else None

    user_response = UserResponse.model_validate(current_user)
    user_response.image_url = image_url 

    return generate_response("success", "User retrieved successfully", user_response)
