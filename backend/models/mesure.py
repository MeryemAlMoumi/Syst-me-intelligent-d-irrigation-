from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Mesure(Base):
    __tablename__ = "mesures"

    id = Column(Integer, primary_key=True, index=True)
    capteur_id = Column(Integer, ForeignKey("capteurs.id"))
    zone_id = Column(Integer, ForeignKey("zones.id"))

    humidite = Column(Float)
    temperature = Column(Float)
    pression = Column(Float)
    debit = Column(Float)

    date_lecture = Column(DateTime, default=datetime.now)

    capteur = relationship("Capteur", back_populates="mesures")
