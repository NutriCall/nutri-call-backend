from pydantic import BaseModel, field_validator

class DailyNutritionResponse(BaseModel):
    goal: float
    daily_carbs: float
    daily_fat: float
    daily_proteins: float
    total_energy: float
    total_carbs: float
    total_fat: float
    total_proteins: float
    
    @field_validator("*", mode="before")
    @classmethod
    def format_values(cls, v, info):
        if isinstance(v, float):
            if info.field_name == "total_energy" or info.field_name == "goal":
                return round(v / 1000, 2)
            return round(v, 2)
        return v
