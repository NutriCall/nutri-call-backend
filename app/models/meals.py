from sqlalchemy import Column, Integer, String, Date
from app.database import Base, engine 

class Meals(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    composition_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(50), nullable=False)
    
Base.metadata.create_all(engine)