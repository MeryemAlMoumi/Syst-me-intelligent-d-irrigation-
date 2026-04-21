from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database import Base

class Meteo(Base):
    __tablename__ = "meteo"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.now)
    temperature = Column(Float)
    humidity = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
