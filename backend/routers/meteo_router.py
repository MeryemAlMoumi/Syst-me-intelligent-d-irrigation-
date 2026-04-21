from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.meteo_service import enregistrer_meteo
from models.meteo import Meteo
import httpx
import os

router = APIRouter(prefix="/weather", tags=["Météo"])


def get_api_key():
    """Recharge complètement la clé API à chaque appel."""
    return os.getenv("OPENWEATHER_API_KEY")


# ---------------------------------------------------------------------
# 1️⃣ Forecast sur 5 jours / Enregistre chaque nouvelle donnée
# ---------------------------------------------------------------------
@router.get("/forecast")
async def get_weather_forecast(lat: float, lon: float, db: Session = Depends(get_db)):

    API_KEY = get_api_key()
    if not API_KEY:
        return {"error": "API key missing"}

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    )

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        data = response.json()

    if "list" not in data:
        return {"error": "OpenWeather error", "details": data}

    forecasts = []

    for i in data["list"]:
        datetime_point = i["dt_txt"]
        temp = i["main"]["temp"]
        humidity = i["main"]["humidity"]

        # Enregistrer dans la BD
        enregistrer_meteo(
            db=db,
            datetime_point=datetime_point,
            temp=temp,
            humidity=humidity,
            lat=lat,
            lon=lon
        )

        forecasts.append({
            "datetime": datetime_point,
            "temperature": temp,
            "humidity": humidity
        })

    return {"forecasts": forecasts}


# ---------------------------------------------------------------------
# 2️⃣ Endpoint pour enregistrer une seule météo (mode simple)
# ---------------------------------------------------------------------
@router.post("/enregistrer")
async def enregistrer_meteo_simple(db: Session = Depends(get_db)):

    API_KEY = get_api_key()
    if not API_KEY:
        return {"error": "API key missing"}

    lat = 33.5731
    lon = -7.5898

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    meteo = Meteo(
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],     # ✔ nom correct
        latitude=lat,
        longitude=lon
    )

    db.add(meteo)
    db.commit()
    db.refresh(meteo)

    return meteo