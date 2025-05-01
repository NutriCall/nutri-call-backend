import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.config import APP_URL
from app.routes import auth, compositions, temporary, meals, recipes, progress, daily_report, weekly_report

app = FastAPI(title="Nutri Call Backend")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(compositions.router, prefix="/api/compositions", tags=["Compositions"])
app.include_router(temporary.router, prefix="/api/temporary", tags=["Temporary"])
app.include_router(meals.router, prefix="/api/meals", tags=["Meals"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["Recipes"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(daily_report.router, prefix="/api/daily-report", tags=["Daily Report"])
app.include_router(weekly_report.router, prefix="/api/weekly-report", tags=["Weekly Report"])

@app.get("/api")
def read_root():
    return {"message": "Welcome to Nutri Call API"}

UPLOAD_DIR = "uploads" 

@app.get("/api/uploads/{file_path:path}")
def get_image(file_path: str):
    file_path = os.path.join(UPLOAD_DIR, file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.get("/check-env")
def check_env():
    return {"APP_URL": APP_URL}
