from sqlalchemy import Column, Integer, String
from app.database import Base, engine 

class TemporaryList(Base):
    __tablename__ = "temporary_list"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    composition_id = Column(Integer, nullable=False)
    date = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    
Base.metadata.create_all(engine)