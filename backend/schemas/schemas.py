from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- BASES (Modèles partagés) ---
class MesureBase(BaseModel):
    humidite: Optional[float]
    temperature: Optional[float]
    debit: Optional[float]
    pression: Optional[float]
    date_lecture: datetime
    class Config:
        from_attributes = True

class CapteurBase(BaseModel):
    nom: str
    type_capteur: str
    mesures: List[MesureBase] = []
    class Config:
        from_attributes = True

class PlanteBase(BaseModel):
    nom: str
    besoin_eau_mm_jour: float
    class Config:
        from_attributes = True

# --- DASHBOARD (/zones) ---
class ZoneDisplay(BaseModel):
    id: int
    nom: str
    # emplacement: Optional[str] = None  # Décommentez si vous utilisez l'emplacement
    plante: Optional[PlanteBase]
    capteurs: List[CapteurBase] = []
    class Config:
        from_attributes = True

# --- IRRIGATION (/irrigation) ---
class IrrigationRow(BaseModel):
    id: int
    zone: str
    date: datetime
    duree: int
    volume: int
    humidite_avant: int
    humidite_apres: int
    gain: int

class IrrigationStats(BaseModel):
    total_arrosages: int
    volume_total: int
    efficacite_moyenne: int

class IrrigationResponse(BaseModel):
    stats: IrrigationStats
    history: List[IrrigationRow]

# --- ALERTES (/alertes) ---
# C'est cette partie qui vous manquait !
class AlerteDisplay(BaseModel):
    id: int
    date: datetime
    zone: str
    capteur: str
    severite: str = "moyenne"
    solution: str
    statut: str
    class Config:
        from_attributes = True