from pydantic import BaseModel

class DailyNutritionResponse(BaseModel):
    goal: float
    daily_carbs: float
    daily_fat: float
    daily_proteins: float
    total_energy: float
    total_carbs: float
    total_fat: float
    total_proteins: float
