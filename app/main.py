import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.config import APP_URL
from app.routes import auth

app = FastAPI(title="Nutri Call Backend")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/api")
def read_root():
    return {"message": "Welcome to Nutri Call API"}

@app.get("/api/uploads/{filename}")
def get_image(filename: str):
    file_path = os.path.join(auth.UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.get("/check-env")
def check_env():
    return {"APP_URL": APP_URL}
