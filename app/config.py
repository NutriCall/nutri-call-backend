import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
APP_URL = os.getenv("APP_URL", "https://byte-together.tech/api")
NGROK_URL = os.getenv("NGROK_URL", "https://byte-together.tech/api")
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 432000 
