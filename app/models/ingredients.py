from sqlalchemy import Column, Integer, String
from app.database import Base, engine 

class Ingredients(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, nullable=False)
    composition_id = Column(Integer, nullable=False)
    
Base.metadata.create_all(engine)