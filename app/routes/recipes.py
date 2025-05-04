from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import date
import shutil
import os
from app.config import NGROK_URL
from app.models.recipes import Recipes
from app.models.ingredients import Ingredients
from app.models.steps import Steps
from app.models.food_compositions import FoodCompositions
from app.schemas.recipes import RecipeListItemSchema, RecipeResponse
from app.schemas.response import ResponseSchema
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

UPLOAD_DIR = "uploads/recipes"

def generate_response(status_message: str, message: str, data=None, status_code: int = 200):
    return ResponseSchema(
        status_message=status_message,
        message=message,
        data=data,
        status_code=status_code
    )

@router.post("/", response_model=ResponseSchema)
def create_recipe(
    name: str = Form(...),
    title: str = Form(...),
    sumber: str = Form(None),
    ingredients: List[int] = Form(...),
    steps: List[str] = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_filename = f"{image.filename}"
    image_path = os.path.join(UPLOAD_DIR, image_filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    image_url = f"/{image_path}".replace("\\", "/")

    total_nutrisi = {
        "air": 0, "energi": 0, "protein": 0, "lemak": 0, "karbohidrat": 0, "serat": 0,
        "abu": 0, "kalsium": 0, "fosfor": 0, "besi": 0, "natrium": 0, "kalium": 0,
        "tembaga": 0, "seng": 0, "retinol": 0, "beta_karoten": 0, "karoten_total": 0,
        "tiamin": 0, "riboflavin": 0, "niasin": 0, "vit_c": 0, "size": 0
    }

    for cid in ingredients:
        food = db.query(FoodCompositions).filter(FoodCompositions.id == cid).first()
        if food:
            for key in total_nutrisi.keys():
                total_nutrisi[key] += getattr(food, key, 0) or 0

    new_recipe = Recipes(
        name=name,
        title=title,
        sumber=sumber,
        user_id=current_user.id,
        date=date.today(),
        image_url=image_url,
        is_published=0,
        **total_nutrisi
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    
    new_composition = FoodCompositions(
        nama_bahan=name,
        sumber=sumber,
        **total_nutrisi
    )
    existing = db.query(FoodCompositions).filter(FoodCompositions.nama_bahan == name).first()
    if not existing:
        db.add(new_composition)
        db.commit()

    for cid in ingredients:
        ingredient = Ingredients(recipe_id=new_recipe.id, composition_id=cid)
        db.add(ingredient)

    for index, step in enumerate(steps):
        step_item = Steps(recipe_id=new_recipe.id, steps=step)
        db.add(step_item)

    db.commit()
    
    response_data = {
        "id": new_recipe.id,
        "composition_id": new_composition.id if not existing else existing.id,
        "name": new_recipe.name,
        "title": new_recipe.title,
        "sumber": new_recipe.sumber,
        "image_url": f"{NGROK_URL}{image_url}",
        "date": new_recipe.date,
        "energi": round(new_recipe.energi / 1000,2),
        "protein": round(new_recipe.protein,2),
        "lemak": round(new_recipe.lemak,2),
        "karbohidrat": round(new_recipe.karbohidrat,2),
        "steps": steps,
        "ingredients": [
            {
                "id": fc.id,
                "nama_bahan": fc.nama_bahan,
            }
            for fc in db.query(FoodCompositions).filter(FoodCompositions.id.in_(ingredients)).all()
        ]
    }

    return generate_response(
        status_message="success",
        message="Recipe created successfully",
        data=response_data
    )

@router.get("/")
def get_recipes(db: Session = Depends(get_db)):
    results = (
        db.query(Recipes, User)
        .join(User, Recipes.user_id == User.id)
        .filter(Recipes.is_published == 1) 
        .all()
    )

    response_data = []
    for recipe, user in results:
        recipe_schema = RecipeListItemSchema(
            id=recipe.id,
            name=recipe.name,
            date=recipe.date,
            image_url=f"{NGROK_URL}{recipe.image_url}" if recipe.image_url else None,
            user_id=recipe.user_id,
            user_full_name=user.full_name,
            user_image=f"{NGROK_URL}{user.image_url}" if user.image_url else None
        )
        response_data.append(recipe_schema)

    return generate_response(
        status_message="success",
        message="Recipes retrieved successfully",
        data=response_data
    )

@router.get("/{recipe_id}", response_model=ResponseSchema)
def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe = (
        db.query(Recipes)
        .filter(Recipes.id == recipe_id)
        .first()
    )

    if not recipe:
        return generate_response(
            status_message="error",
            message="Recipe not found",
            data=None,
            status_code=404
        )

    user = db.query(User).filter(User.id == recipe.user_id).first()

    ingredients = (
        db.query(Ingredients, FoodCompositions)
        .join(FoodCompositions, Ingredients.composition_id == FoodCompositions.id)
        .filter(Ingredients.recipe_id == recipe_id)
        .all()
    )

    steps = (
        db.query(Steps)
        .filter(Steps.recipe_id == recipe_id)
        .order_by(Steps.id)
        .all()
    )
    
    matching_food = (
        db.query(FoodCompositions)
        .filter(FoodCompositions.nama_bahan == recipe.name)
        .first()
    )

    response_data = {
        "id": recipe.id,
        "composition_id": matching_food.id if matching_food else None,
        "name": recipe.name,
        "title": recipe.title,
        "sumber": recipe.sumber,
        "image_url": f"{NGROK_URL}{recipe.image_url}" if recipe.image_url else None,
        "date": recipe.date,
        "energi": round(recipe.energi / 1000, 2),
        "protein": round(recipe.protein, 2),
        "lemak": round(recipe.lemak, 2),
        "karbohidrat": round(recipe.karbohidrat, 2),
        "ingredients": [
            {
                "id": fc.id,
                "nama_bahan": fc.nama_bahan,
            }
            for _, fc in ingredients
        ],
        "steps": [step.steps for step in steps]
    }

    return generate_response(
        status_message="success",
        message="Recipe retrieved successfully",
        data=response_data
    )

@router.post("/publish/{recipe_id}", response_model=ResponseSchema)
def publish_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipes).filter(Recipes.id == recipe_id).first()

    if not recipe:
        return generate_response(
            status_message="error",
            message="Recipe not found",
            data=None,
            status_code=404
        )

    recipe.is_published = 1
    db.commit()

    return generate_response(
        status_message="success",
        message="Recipe published successfully",
        data=None
    )