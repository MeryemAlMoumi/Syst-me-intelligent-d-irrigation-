from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    plante_id = Column(Integer, ForeignKey("plantes.id"))

    plante = relationship("Plante", back_populates="zones")
    capteurs = relationship("Capteur", back_populates="zone")
