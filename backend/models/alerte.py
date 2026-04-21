from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Alerte(Base):
    __tablename__ = "alertes"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"))
    capteur_id = Column(Integer, ForeignKey("capteurs.id"))

    type_probleme = Column(String)
    message_resolution = Column(Text)

    date_alerte = Column(DateTime, default=datetime.now)
