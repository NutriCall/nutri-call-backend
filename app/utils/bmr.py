def calculate_goal_bmr(age: int, weight: int, height: int, gender: str, aktivitas: str) -> float:
    fa_map = {
        "Little Activity/No Exercise": 1.2,
        "Light Activity": 1.375,
        "Moderate Activity": 1.55,
        "High Activity": 1.725
    }

    if aktivitas not in fa_map:
        raise ValueError("Aktivitas tidak valid")

    fa = fa_map[aktivitas]

    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender == "Female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("Gender tidak valid")

    goal = bmr * fa
    return round(goal, 2)

def calculate_daily_carbs(goal: float) -> float:
    daily_carbs = (60 / 100 * goal) / 4
    return round(daily_carbs, 2)

def calculate_daily_fat(goal: float) -> float:
    daily_fat = (15 /100 * goal) / 4
    return round(daily_fat, 2)

def calculate_daily_proteins(goal: float) -> float:
    daily_proteins = (25 /100 * goal) / 9
    return round(daily_proteins, 2)
