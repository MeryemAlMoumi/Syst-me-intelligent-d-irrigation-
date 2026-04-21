from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Plante(Base):
    __tablename__ = "plantes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    besoin_eau_mm_jour = Column(Float)

    zones = relationship("Zone", back_populates="plante")
