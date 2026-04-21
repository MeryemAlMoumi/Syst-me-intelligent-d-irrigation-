from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from dotenv import load_dotenv
import os

# --- Imports des Modèles (pour la création des tables) ---
from models.capteur import Capteur
from models.alerte import Alerte
from models.mesure import Mesure
from models.plante import Plante
from models.zone import Zone
from models.meteo import Meteo

# --- Imports de TOUS VOS ROUTERS ---
from routers import (
    ai_router, 
    alertes_router, 
    mesures_router, 
    meteo_router,
    dashboard_router,   # Votre route GET /zones
    irrigation_router   # Votre route GET /irrigation
)

load_dotenv()
# La connexion DB est définie dans database.py

# Création des tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroSmart API",
    description="API Smart Irrigation & AI",
    version="1.0"
)

# --- Configuration CORS (Obligatoire pour le lien Front/Back) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Autorise toute origine (pour le développement)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusion des routes ---
app.include_router(dashboard_router.router)   # GET /zones
app.include_router(irrigation_router.router)  # GET /irrigation
app.include_router(alertes_router.router)     # GET /alertes et POST /alertes/analyse-et-enregistrer
app.include_router(ai_router.router)          # GET /ai/...
app.include_router(mesures_router.router)     # POST /mesures/receive
app.include_router(meteo_router.router)       # GET /weather/forecast

@app.get("/")
def root():
    return {"message": "API AgroSmart en ligne 🚀"}