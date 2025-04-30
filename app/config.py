import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@127.0.0.1:3307/nutri_app")
APP_URL = os.getenv("APP_URL", "http://localhost:8878/api")
NGROK_URL = os.getenv("NGROK_URL")
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 
