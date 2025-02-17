from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.response import ResponseSchema
from app.utils.security import get_current_user, hash_password, verify_password, create_access_token

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

@router.put("/edit-profile", response_model=ResponseSchema[UserResponse])
def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    for key, value in user_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    user_response = UserResponse.model_validate(current_user)
    return generate_response("success", "Profile updated successfully", user_response)