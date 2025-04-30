from sqlalchemy import Column, Integer, Date
from app.database import Base, engine 

class WeightHistory(Base):
    __tablename__ = "weight_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=True)
    date = Column(Date, nullable=True)
    
Base.metadata.create_all(engine)