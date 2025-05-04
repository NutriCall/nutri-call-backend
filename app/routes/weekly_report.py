from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models.user import User
from app.models.meals import Meals
from app.models.food_compositions import FoodCompositions
from app.routes.auth import get_current_user
from app.schemas.response import ResponseSchema
from app.schemas.weekly_report import WeeklyCaloriesResponse, WeeklyEatenResponse, WeeklyMacroPercentage

router = APIRouter()

def generate_response(status_message: str, message: str, data=None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.get("/calories", response_model=ResponseSchema[WeeklyCaloriesResponse])
def get_weekly_calories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    goal_per_day = current_user.goal or 0
    total_weekly_goal = goal_per_day * 7

    meals = (
        db.query(Meals, FoodCompositions)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date >= start_of_week,
            Meals.date <= end_of_week
        )
        .all()
    )

    total_energy = sum((food.energi or 0) for _, food in meals)

    return generate_response(
        status_message="success",
        message="Weekly calories summary retrieved",
        data=WeeklyCaloriesResponse(
            weekly_goal=round(total_weekly_goal, 2),
            weekly_consumed=round(total_energy, 2),
            difference=round(total_weekly_goal - total_energy, 2)
        )
    )

@router.get("/eaten", response_model=ResponseSchema[WeeklyEatenResponse])
def get_weekly_eaten_macros(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    meals = (
        db.query(FoodCompositions.karbohidrat, FoodCompositions.lemak, FoodCompositions.protein)
        .join(Meals, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date >= start_of_week,
            Meals.date <= end_of_week
        )
        .all()
    )

    total_carbs = sum([m.karbohidrat or 0 for m in meals])
    total_fats = sum([m.lemak or 0 for m in meals])
    total_proteins = sum([m.protein or 0 for m in meals])

    total_macros = total_carbs + total_fats + total_proteins

    def calc_percentage(value):
        return round((value / total_macros) * 100, 2) if total_macros > 0 else 0

    items = [
        WeeklyMacroPercentage(name="Karbohidrat", total=round(total_carbs, 2), percentage=calc_percentage(total_carbs)),
        WeeklyMacroPercentage(name="Lemak", total=round(total_fats, 2), percentage=calc_percentage(total_fats)),
        WeeklyMacroPercentage(name="Protein", total=round(total_proteins, 2), percentage=calc_percentage(total_proteins)),
    ]

    return generate_response(
        status_message="success",
        message="Weekly macros retrieved",
        data=WeeklyEatenResponse(items=items)
    )
    
@router.get("/graph-calories", response_model=ResponseSchema)
def get_weekly_graph_calories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    meals = (
        db.query(Meals.date, func.sum(FoodCompositions.energi).label('total_energy'))
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date >= start_of_week,
            Meals.date <= end_of_week
        )
        .group_by(Meals.date)
        .all()
    )

    goal_energi = current_user.goal or 0  

    graph_data = []
    
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        
        meal_data = next((meal for meal in meals if meal.date == day), None)
        
        if meal_data:
            total_energy = meal_data.total_energy or 0
        else:
            total_energy = 0
        
        percentage_of_goal = (total_energy / goal_energi) * 100 if goal_energi > 0 else 0
        
        graph_data.append({
            "date": day.isoformat(),
            "total_energy": round(total_energy, 2),
            "percentage_of_goal": round(percentage_of_goal, 2)
        })

    return generate_response(
        status_message="success",
        message="Weekly graph-calories report retrieved successfully",
        data={"graph": graph_data}
    )
    
@router.get("/resume", response_model=ResponseSchema)
def get_weekly_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)

    meals = (
        db.query(
            func.sum(FoodCompositions.air).label('total_air'),
            func.sum(FoodCompositions.energi).label('total_energi'),
            func.sum(FoodCompositions.protein).label('total_protein'),
            func.sum(FoodCompositions.lemak).label('total_lemak'),
            func.sum(FoodCompositions.karbohidrat).label('total_karbohidrat'),
            func.sum(FoodCompositions.serat).label('total_serat'),
            func.sum(FoodCompositions.abu).label('total_abu'),
            func.sum(FoodCompositions.kalsium).label('total_kalsium'),
            func.sum(FoodCompositions.fosfor).label('total_fosfor'),
            func.sum(FoodCompositions.besi).label('total_besi'),
            func.sum(FoodCompositions.natrium).label('total_natrium'),
            func.sum(FoodCompositions.tembaga).label('total_tembaga'),
            func.sum(FoodCompositions.seng).label('total_seng'),
            func.sum(FoodCompositions.retinol).label('total_retinol'),
            func.sum(FoodCompositions.beta_karoten).label('total_beta_karoten'),
            func.sum(FoodCompositions.karoten_total).label('total_karoten_total'),
            func.sum(FoodCompositions.kalium).label('total_kalium'),
            func.sum(FoodCompositions.tiamin).label('total_tiamin'),
            func.sum(FoodCompositions.riboflavin).label('total_riboflavin'),
            func.sum(FoodCompositions.niasin).label('total_niasin'),
            func.sum(FoodCompositions.vit_c).label('total_vit_c'),
        )
        .select_from(Meals)
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(
            Meals.user_id == current_user.id,
            Meals.date >= start_of_week,
            Meals.date <= end_of_week
        )
        .first()
    )

    total_data = {key: getattr(meals, key) or 0 for key in meals._fields}

    total_all = round(sum(total_data.values()), 2)

    nutrient_percentage = {
        key: round((value / total_all) * 100) if total_all > 0 else 0
        for key, value in total_data.items()
    }

    return generate_response(
        status_message="success",
        message="Weekly resume report retrieved successfully",
        data={
            "total_all": total_all,
            "nutrient_percentage": nutrient_percentage
        }
    )
