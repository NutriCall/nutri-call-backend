from sqlalchemy import Column, Integer, String, Float
from app.database import Base, engine 

class FoodCompositions(Base):
    __tablename__ = "food_compositions"
    
    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(50), nullable=True)
    nama_bahan = Column(String(255), nullable=False)
    sumber = Column(String(255), nullable=True)
    air = Column(Float, nullable=True)
    energi = Column(Float, nullable=True) 
    protein = Column(Float, nullable=True)
    lemak = Column(Float, nullable=True)
    karbohidrat = Column(Float, nullable=True)
    serat = Column(Float, nullable=True)
    abu = Column(Float, nullable=True)
    kalsium = Column(Float, nullable=True)
    fosfor = Column(Float, nullable=True)
    besi = Column(Float, nullable=True)
    natrium = Column(Float, nullable=True)
    kalium = Column(Float, nullable=True)
    tembaga = Column(Float, nullable=True)
    seng = Column(Float, nullable=True)
    retinol = Column(Float, nullable=True)
    beta_karoten = Column(Float, nullable=True)
    karoten_total = Column(Float, nullable=True)
    tiamin = Column(Float, nullable=True)
    riboflavin = Column(Float, nullable=True)
    niasin = Column(Float, nullable=True)
    vit_c = Column(Float, nullable=True)
    bdd = Column(Float, nullable=True)
    size = Column(Float, nullable=True)

Base.metadata.create_all(engine)
    
    
    