from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models.user import User
from app.models.meals import Meals
from app.models.food_compositions import FoodCompositions
from app.schemas.report import DailyCaloriesResponse, FoodEatenResponse, FoodEatenItem, FoodEatenTotal, MacroResponse, NutrientReport, NutrientItem
from sqlalchemy import func
from fastapi.security import OAuth2PasswordBearer
from app.routes.auth import get_current_user 
from app.schemas.response import ResponseSchema

router = APIRouter()

def generate_response(status_message: str, message: str, data=None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.get("/calories", response_model=ResponseSchema[DailyCaloriesResponse])
def get_daily_calories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    meals_today = (
        db.query(Meals)
        .filter(Meals.user_id == current_user.id, Meals.date == today)
        .all()
    )

    total_calories = 0
    type_calories = {"Breakfast": 0, "Lunch": 0, "Dinner": 0, "Snacks/Other": 0}

    for meal in meals_today:
        if meal.composition_id:
            composition = db.query(FoodCompositions).filter(FoodCompositions.id == meal.composition_id).first()
            if composition:
                energi = composition.energi or 0
                total_calories += energi
                meal_type = meal.type
                if meal_type not in type_calories:
                    meal_type = "Snacks/Other"
                type_calories[meal_type] += energi

    today_calories = []
    for meal_type, cal in type_calories.items():
        percentage = (cal / total_calories) * 100 if total_calories > 0 else 0
        today_calories.append({
            "type": meal_type,
            "calories": cal,
            "percentage": round(percentage, 2)
        })
        
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    meals_week = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date >= start_of_week,
            Meals.date <= end_of_week
        )
        .all()
    )

    graph_data = {}
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        graph_data[day] = {
            "date": day.isoformat(),
            "Breakfast": 0,
            "Lunch": 0,
            "Dinner": 0,
            "Snacks/Other": 0
        }
        
    total_weekly_energy = 0

    for meal, composition in meals_week:
        energi = composition.energi or 0
        total_weekly_energy += energi
        meal_date = meal.date
        meal_type = meal.type if meal.type in graph_data[meal_date] else "Snacks/Other"
        graph_data[meal_date][meal_type] += energi

    average = round(total_weekly_energy / 7, 2)
    graph = list(graph_data.values())

    data = DailyCaloriesResponse(
        goal=current_user.goal or 0,
        total_cal_today=total_calories,
        average=average,
        today_calories=today_calories,
        graph=graph
    )

    return generate_response(
        status_message="success",
        message="Daily calorie report retrieved successfully",
        data=data
    )

@router.get("/food-eaten", response_model=ResponseSchema[FoodEatenResponse])
def get_food_eaten_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    meals_today = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date == today
        )
        .all()
    )

    food_counter = {}

    for meal, composition in meals_today:
        if not composition.nama_bahan:
            continue
        key = composition.nama_bahan
        energi = composition.energi or 0
        fats = composition.lemak or 0
        carbs = composition.karbohidrat or 0
        protein = composition.protein or 0

        if key not in food_counter:
            food_counter[key] = {"count": 0, "total_calories": 0, "total_fats": 0, "total_carbs": 0, "total_proteins": 0}
        
        food_counter[key]["count"] += 1
        food_counter[key]["total_calories"] += energi
        food_counter[key]["total_fats"] += fats
        food_counter[key]["total_carbs"] += carbs
        food_counter[key]["total_proteins"] += protein

    items = [
        FoodEatenItem(
            nama_bahan=nama_bahan,
            count=data["count"],
            total_calories=round(data["total_calories"], 2),
            total_fats=round(data["total_fats"], 2),
            total_carbs=round(data["total_carbs"], 2),
            total_proteins=round(data["total_proteins"], 2)
        )
        for nama_bahan, data in food_counter.items()
    ]

    total_count = 0
    total_calories_all = 0
    total_fats_all = 0
    total_carbs_all = 0
    total_proteins_all = 0

    items = []
    for nama_bahan, data in food_counter.items():
        total_count += data["count"]
        total_calories_all += data["total_calories"]
        total_fats_all += data["total_fats"]
        total_carbs_all += data["total_carbs"]
        total_proteins_all += data["total_proteins"]
        items.append(FoodEatenItem(
            nama_bahan=nama_bahan,
            count=data["count"],
            total_calories=round(data["total_calories"], 2),
            total_carbs=round(data["total_carbs"], 2),
            total_fats=round(data["total_fats"], 2),
            total_proteins=round(data["total_proteins"], 2)
        ))
    
    items.append(FoodEatenItem(
        nama_bahan="Total",
        count=total_count,
        total_calories=round(total_calories_all, 2),
        total_fats=round(total_fats_all, 2),
        total_carbs=round(total_carbs_all, 2),
        total_proteins=round(total_proteins_all, 2)
    ))

    total = FoodEatenTotal(
        count=total_count,
        total_calories=round(total_calories_all, 2),
        total_fats=round(total_fats_all, 2),
        total_carbs=round(total_carbs_all, 2),
        total_proteins=round(total_proteins_all, 2)
    )

    return generate_response(
        status_message="success",
        message="Food eaten today retrieved successfully",
        data=FoodEatenResponse(items=items, total=total)
    )

@router.get("/macro", response_model=ResponseSchema[MacroResponse])
def get_macronutrient_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    meals_week = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date >= start_of_week,
            Meals.date <= end_of_week
        )
        .all()
    )

    graph_data = {}
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        graph_data[day] = {
            "date": day.isoformat(),
            "carbs": 0,
            "proteins": 0,
            "fats": 0
        }

    for meal, composition in meals_week:
        meal_date = meal.date
        graph_data[meal_date]["carbs"] += composition.karbohidrat or 0
        graph_data[meal_date]["proteins"] += composition.protein or 0
        graph_data[meal_date]["fats"] += composition.lemak or 0

    graph = list(graph_data.values())

    meals_today = [
        (m, f) for m, f in meals_week if m.date == today
    ]

    total_carbs = sum(f.karbohidrat or 0 for _, f in meals_today)
    total_proteins = sum(f.protein or 0 for _, f in meals_today)
    total_fats = sum(f.lemak or 0 for _, f in meals_today)

    target_carbs = current_user.daily_carbs or 1
    target_proteins = current_user.daily_proteins or 1
    target_fats = current_user.daily_fat or 1

    today_macro = {
        "carbs": {
            "value": round(total_carbs, 2),
            "percentage": round((total_carbs / target_carbs) * 100, 2)
        },
        "proteins": {
            "value": round(total_proteins, 2),
            "percentage": round((total_proteins / target_proteins) * 100, 2)
        },
        "fats": {
            "value": round(total_fats, 2),
            "percentage": round((total_fats / target_fats) * 100, 2)
        }
    }

    return {
        "status_message": "success",
        "message": "Macronutrient report generated successfully",
        "data": {
            "graph": graph,
            "today_macro": today_macro
        },
        "status_code": 200
    }
    
@router.get("/nutrien", response_model=ResponseSchema[NutrientReport])
def get_nutrient_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    meals_today = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(Meals.user_id == current_user.id, Meals.date == today)
        .all()
    )

    nutrient_fields = [
        "air", "energi", "protein", "lemak", "karbohidrat", "serat", "abu",
        "kalsium", "fosfor", "besi", "natrium", "kalium", "tembaga", "seng",
        "retinol", "beta_karoten", "karoten_total", "tiamin", "riboflavin",
        "niasin", "vit_c"
    ]

    nutrient_totals = {field: 0.0 for field in nutrient_fields}

    for _, food in meals_today:
        for field in nutrient_fields:
            value = getattr(food, field) or 0.0
            nutrient_totals[field] += value

    user_goals = {
        "energi": current_user.goal,
        "lemak": current_user.daily_fat,
        "karbohidrat": current_user.daily_carbs,
        "protein": current_user.daily_proteins
    }

    nutrient_items = []

    for field in nutrient_fields:
        consumed = round(nutrient_totals[field], 2)
        goal = user_goals.get(field, "-")
        if isinstance(goal, (int, float)):
            difference = round(goal - consumed, 2)
        else:
            difference = "-"
        nutrient_items.append(NutrientItem(
            name=field,
            consumed=consumed,
            goal=goal if goal != None else "-",
            difference=difference
        ))

    report = NutrientReport(nutrients=nutrient_items)

    return generate_response(
        status_message="success",
        message="Nutrient report for today",
        data=report
    )