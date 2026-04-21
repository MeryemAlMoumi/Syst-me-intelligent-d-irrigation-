from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Capteur(Base):
    __tablename__ = "capteurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    type_capteur = Column(String)
    zone_id = Column(Integer, ForeignKey("zones.id"))

    zone = relationship("Zone", back_populates="capteurs")
    mesures = relationship("Mesure", back_populates="capteur")
