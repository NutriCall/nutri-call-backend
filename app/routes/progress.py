from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
import random
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User
from app.models.meals import Meals
from app.models.weight_history import WeightHistory
from app.models.food_compositions import FoodCompositions
from app.schemas.progress import DailyNutritionResponse
from app.schemas.response import ResponseSchema

router = APIRouter()

def generate_response(status_message: str, message: str, data=None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.get("/nutritions", response_model=ResponseSchema)
def get_nutrition_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    meals = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(Meals.user_id == current_user.id, Meals.date == today)
        .all()
    )

    total_energy = total_carbs = total_fat = total_proteins = 0

    for _, food in meals:
        total_energy += food.energi or 0
        total_carbs += food.karbohidrat or 0
        total_fat += food.lemak or 0
        total_proteins += food.protein or 0
        
    goal = current_user.goal or 0
    difference_energy = goal - total_energy if goal else 0
    percentage_energy = round((total_energy / goal) * 100, 2) if goal else 0

    data = {
        "goal": goal,
        "daily_carbs": current_user.daily_carbs or 0,
        "daily_fat": current_user.daily_fat or 0,
        "daily_proteins": current_user.daily_proteins or 0,
        "total_energy": total_energy,
        "total_carbs": total_carbs,
        "total_fat": total_fat,
        "total_proteins": total_proteins,
        "difference_energy": difference_energy,
        "percentage_energy": percentage_energy,
    }

    return generate_response(
        status_message="success",
        message="Nutrition data retrieved successfully",
        data=data
    )
    
@router.get("/weight", response_model=ResponseSchema)
def get_weight_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    histories = (
        db.query(WeightHistory)
        .filter(WeightHistory.user_id == current_user.id)
        .order_by(WeightHistory.date.desc())
        .limit(5)
        .all()
    )

    traffic = []
    dates_used = set()
    last_weight = current_user.weight

    for h in histories:
        date_obj = h.date if isinstance(h.date, date) else h.date.date()
        traffic.append({
            "date": str(date_obj),
            "weight": h.weight
        })
        dates_used.add(date_obj)
        last_weight = h.weight  

    additional_needed = 5 - len(traffic)
    while additional_needed > 0:
        random_days_ago = random.randint(1, 14)
        generated_date = today - timedelta(days=random_days_ago)
        if generated_date not in dates_used:
            traffic.append({
                "date": str(generated_date),
                "weight": last_weight
            })
            dates_used.add(generated_date)
            additional_needed -= 1

    # Sortir berdasarkan tanggal menaik
    traffic.sort(key=lambda x: x["date"])

    result = {
        "weight": current_user.weight,
        "weight_target": current_user.weight_target,
        "date": str(today),
        "traffic": traffic
    }

    return generate_response(
        status_message="success",
        message="Weight progress data retrieved successfully",
        data=result
    )

@router.get("/cal-today", response_model=ResponseSchema)
def get_calories_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    meals = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(Meals.user_id == current_user.id, Meals.date == today)
        .all()
    )

    total_energy = sum((food.energi or 0) for _, food in meals)
    user_goal = current_user.goal or 0

    return generate_response(
        status_message="success",
        message="Calories consumed today",
        data={"calories": total_energy, "goal": user_goal}
    )