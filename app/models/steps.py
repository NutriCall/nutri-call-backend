from sqlalchemy import Column, Integer, String, Float
from app.database import Base, engine 

class Steps(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, nullable=False)
    steps = Column(String(255), nullable=False)
    
Base.metadata.create_all(engine)