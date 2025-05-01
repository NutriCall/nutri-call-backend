import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
APP_URL = os.getenv("APP_URL", "http://178.128.30.50:8000/api")
NGROK_URL = os.getenv("NGROK_URL", "http://178.128.30.50:8000/api")
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 432000 
