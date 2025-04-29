def calculate_goal_bmr(age: int, weight: int, height: int, gender: str, aktivitas: str) -> float:
    fa_map = {
        "Sedikit/Tidak Berolahraga": 1.2,
        "Aktivitas Ringan": 1.375,
        "Aktivitas Sedang": 1.55,
        "Aktivitas Tinggi": 1.725
    }

    if aktivitas not in fa_map:
        raise ValueError("Aktivitas tidak valid")

    fa = fa_map[aktivitas]

    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender.lower() == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("Gender tidak valid")

    goal = bmr * fa
    return round(goal, 2)
