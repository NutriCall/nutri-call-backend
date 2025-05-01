from pydantic import BaseModel
from typing import Optional

class WeeklyCaloriesResponse(BaseModel):
    weekly_goal: float
    weekly_consumed: float
    difference: float


class WeeklyMacroPercentage(BaseModel):
    name: str
    total: float
    percentage: float

class WeeklyEatenResponse(BaseModel):
    items: list[WeeklyMacroPercentage]
    