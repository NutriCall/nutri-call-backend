from pydantic import BaseModel
from typing import List, Dict, Union

class MealTypeCalories(BaseModel):
    type: str
    calories: float
    percentage: float

class DailyCaloriesResponse(BaseModel):
    goal: float
    total_cal_today: float
    today_calories: List[MealTypeCalories]
    average: float
    graph: List[Dict[str, Union[str, float]]] 
    

class FoodEatenItem(BaseModel):
    nama_bahan: str
    count: int
    total_calories: float
    total_fats: float
    total_carbs: float
    total_proteins: float

class FoodEatenTotal(BaseModel):
    count: int
    total_calories: float
    total_fats: float
    total_carbs: float
    total_proteins: float

class FoodEatenResponse(BaseModel):
    items: List[FoodEatenItem]
    total: FoodEatenTotal
    
class MacroGraphItem(BaseModel):
    date: str
    carbs: float
    proteins: float
    fats: float

class MacroDetail(BaseModel):
    value: float
    percentage: float

class TodayMacro(BaseModel):
    carbs: MacroDetail
    proteins: MacroDetail
    fats: MacroDetail

class MacroResponse(BaseModel):
    graph: List[MacroGraphItem]
    today_macro: TodayMacro

class NutrientItem(BaseModel):
    name: str
    consumed: float
    goal: Union[float, str] 
    difference: Union[float, str]  

class NutrientReport(BaseModel):
    nutrients: List[NutrientItem]