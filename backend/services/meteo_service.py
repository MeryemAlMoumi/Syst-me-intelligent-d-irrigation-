from sqlalchemy.orm import Session
from models.meteo import Meteo
from datetime import datetime

def enregistrer_meteo(db: Session, datetime_point: datetime, temp: float, humidity: float, lat: float, lon: float) -> Meteo:
    meteo = Meteo(
        datetime=datetime_point,
        temperature=temp,
        humidity=humidity,
        latitude=lat,
        longitude=lon
    )
    db.add(meteo)
    db.commit()
    db.refresh(meteo)
    return meteo
