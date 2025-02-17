from fastapi import FastAPI
from app.routes import auth

app = FastAPI(title="Nutri Call Backend")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/api")
def read_root():
    return {"message": "Welcome to Nutri Call API"}

