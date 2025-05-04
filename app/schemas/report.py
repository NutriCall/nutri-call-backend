from pydantic import BaseModel, field_validator
from typing import List, Dict, Union

class MealTypeCalories(BaseModel):
    type: str
    calories: float
    percentage: float
    
    @field_validator("calories", "percentage", mode="before")
    @classmethod
    def round_float(cls, v): return round(v, 2) if isinstance(v, float) else v

class DailyCaloriesResponse(BaseModel):
    goal: float
    total_cal_today: float
    today_calories: List[MealTypeCalories]
    average: float
    graph: List[Dict[str, Union[str, float]]] 
    
    @field_validator("goal", "total_cal_today", "average", mode="before")
    @classmethod
    def divide_and_round(cls, v):
        return round(v / 1000, 2) if isinstance(v, float) else v
    

class FoodEatenItem(BaseModel):
    nama_bahan: str
    count: int
    total_calories: float
    total_fats: float
    total_carbs: float
    total_proteins: float
    
    @field_validator("*", mode="before")
    @classmethod
    def round_vals(cls, v): return round(v, 2) if isinstance(v, float) else v

class FoodEatenTotal(BaseModel):
    count: int
    total_calories: float
    total_fats: float
    total_carbs: float
    total_proteins: float
    
    @field_validator("*", mode="before")
    @classmethod
    def round_vals(cls, v): return round(v, 2) if isinstance(v, float) else v

class FoodEatenResponse(BaseModel):
    items: List[FoodEatenItem]
    total: FoodEatenTotal
    
class MacroGraphItem(BaseModel):
    date: str
    carbs: float
    proteins: float
    fats: float
    
    @field_validator("*", mode="before")
    @classmethod
    def round_vals(cls, v): return round(v, 2) if isinstance(v, float) else v

class MacroDetail(BaseModel):
    value: float
    percentage: float
    
    @field_validator("*", mode="before")
    @classmethod
    def round_vals(cls, v): return round(v, 2) if isinstance(v, float) else v

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
    
    @field_validator("consumed", mode="before")
    @classmethod
    def round_consumed(cls, v, info):
        if info.data.get("name") == "energi" and isinstance(v, float):
            return round(v / 1000, 2)
        return round(v, 2) if isinstance(v, float) else v

    @field_validator("goal", "difference", mode="before")
    @classmethod
    def round_optional(cls, v, info):
        if info.data.get("name") == "energi" and isinstance(v, float):
            return round(v / 1000, 2)
        return round(v, 2) if isinstance(v, float) else v

class NutrientReport(BaseModel):
    nutrients: List[NutrientItem]