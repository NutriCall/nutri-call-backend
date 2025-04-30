from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.temporary_list import TemporaryList
from app.models.meals import Meals
from app.models.food_compositions import FoodCompositions
from app.models.user import User
from app.schemas.meals import MealsCreate, MealsResponse, MealsWithDetailsResponse, MealsWithTotalEnergyResponse, FoodCompositionDetails
from app.schemas.response import ResponseSchema
from app.routes.auth import get_current_user
from datetime import date

router = APIRouter()

def generate_response(status_message: str, message: str, data=None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.post("/move-to-meals", response_model=ResponseSchema[list[MealsResponse]])
def move_to_meals(
    type: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    temp_items = (
        db.query(TemporaryList)
        .filter(
            TemporaryList.user_id == current_user.id,
            TemporaryList.date == today,
            TemporaryList.type == type
        )
        .all()
    )

    if not temp_items:
        raise HTTPException(status_code=404, detail="No temporary items found for this type")

    meals_data = []

    for item in temp_items:
        meal_item = Meals(
            user_id=item.user_id,
            composition_id=item.composition_id,
            date=item.date,
            type=item.type
        )

        db.add(meal_item)

    db.commit() 

    for item in temp_items:
        meal_item = db.query(Meals).filter(Meals.user_id == item.user_id, Meals.composition_id == item.composition_id).first()
        meals_data.append(MealsResponse.from_orm(meal_item))

    db.query(TemporaryList).filter(
        TemporaryList.user_id == current_user.id,
        TemporaryList.date == today,
        TemporaryList.type == type
    ).delete()

    db.commit()

    return generate_response(
        status_message="success",
        message=f"Temporary items moved to meals for {type}",
        data=meals_data
    )

@router.get("/", response_model=ResponseSchema[list[MealsWithTotalEnergyResponse]])
def get_meals_for_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    meals_data = (
        db.query(
            Meals.id,
            Meals.user_id,
            Meals.composition_id,
            Meals.date,
            Meals.type,
            FoodCompositions.nama_bahan,
            FoodCompositions.energi,
            FoodCompositions.karbohidrat,
            FoodCompositions.protein,
            FoodCompositions.lemak
        )
        .join(FoodCompositions, Meals.composition_id == FoodCompositions.id)
        .filter(Meals.user_id == current_user.id, Meals.date == today)
        .all()
    )

    meals_by_type = {
        "Breakfast": [],
        "Lunch": [],
        "Dinner": [],
        "Snacks/Other": []
    }

    type_energi_totals = {key: 0 for key in meals_by_type.keys()}

    for meal in meals_data:
        meal_detail = MealsWithDetailsResponse(
            id=meal.id,
            user_id=meal.user_id,
            composition_id=meal.composition_id,
            date=meal.date,
            type=meal.type,
            food_composition=FoodCompositionDetails(
                nama_bahan=meal.nama_bahan,
                energi=meal.energi,
                karbohidrat=meal.karbohidrat,
                protein=meal.protein,
                lemak=meal.lemak
            )
        )

        meals_by_type[meal.type].append(meal_detail)
        type_energi_totals[meal.type] += meal.energi

    response_data = []

    for meal_type in ["Breakfast", "Lunch", "Dinner", "Snacks/Other"]:
        response_data.append(
            MealsWithTotalEnergyResponse(
                type=meal_type,
                meals=meals_by_type[meal_type],
                total_energi=type_energi_totals[meal_type]
            )
        )

    return generate_response(
        status_message="success",
        message="Meals data for today",
        data=response_data
    )
    
@router.delete("/delete/{meal_id}", response_model=ResponseSchema[MealsResponse])
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal_item = db.query(Meals).filter(Meals.id == meal_id, Meals.user_id == current_user.id).first()

    if not meal_item:
        raise HTTPException(status_code=404, detail="Meal not found")

    db.delete(meal_item)
    db.commit()

    return generate_response(
        status_message="success",
        message="Meal deleted successfully",
        data=MealsResponse.from_orm(meal_item)
    )

@router.post("/add", response_model=ResponseSchema[List[MealsResponse]])
def add_meal(
    body: MealsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    new_meals = []

    for composition_id in body.compositions:
        new_meal = Meals(
            user_id=current_user.id,
            composition_id=composition_id,
            date=today,
            type=body.type
        )
        db.add(new_meal)
        new_meals.append(new_meal)

    db.commit()

    for meal in new_meals:
        db.refresh(meal)

    db.query(TemporaryList).filter(
        TemporaryList.user_id == current_user.id,
        TemporaryList.date == today,
        TemporaryList.type == body.type,
        TemporaryList.composition_id.in_(body.compositions)
    ).delete(synchronize_session=False)

    db.commit()

    return generate_response(
        status_message="success",
        message="Meals added successfully",
        data=[MealsResponse.from_orm(meal) for meal in new_meals]
    )
