from sqlalchemy import Column, Integer, String, Float
from app.database import Base, engine 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False) 
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    weight_target = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)  
    bmi = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=True)
    fa = Column(String(255), nullable=True)
    goal = Column(Float, nullable=True) 

Base.metadata.create_all(engine)
