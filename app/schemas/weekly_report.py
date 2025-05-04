from pydantic import BaseModel, field_validator

class WeeklyCaloriesResponse(BaseModel):
    weekly_goal: float
    weekly_consumed: float
    difference: float
    
    @field_validator("*", mode="before")
    @classmethod
    def format_values(cls, v, info):
        if isinstance(v, float):
            if info.field_name == "weekly_goal" or info.field_name == "weekly_consumed" or info.field_name == "difference":
                return round(v / 1000, 2)
            return round(v, 2)
        return v


class WeeklyMacroPercentage(BaseModel):
    name: str
    total: float
    percentage: float

class WeeklyEatenResponse(BaseModel):
    items: list[WeeklyMacroPercentage]
    