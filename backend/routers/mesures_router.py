from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.service_mesure import enregistrer_mesure
from services.ai_service import analyser_par_ai
from services.alerte_service import creer_alerte

router = APIRouter(prefix="/mesures", tags=["Mesures"])

@router.post("/receive")
def recevoir_mesure(data: dict, db: Session = Depends(get_db)):

    pression = data["pression"]
    debit = data["debit"]
    humidite = data["humidite"]
    zone_id = data["zone_id"]
    capteur_id = data["capteur_id"]

    # 1️⃣ Enregistrer la mesure dans DB
    mesure = enregistrer_mesure(
        db=db,
        capteur_id=capteur_id,
        zone_id=zone_id,
        pression=pression,
        debit=debit,
        humidite=humidite
    )

    # 2️⃣ Analyser par IA
    resultat = analyser_par_ai(pression, debit, humidite)

    # 3️⃣ Si anomalie → création alerte
    if resultat["anomalie"] != "normal":
        alerte = creer_alerte(
            db=db,
            zone_id=zone_id,
            capteur_id=capteur_id,
            type_probleme=resultat["anomalie"],
            message_resolution=resultat["solution"]
        )
        resultat["alerte_id"] = alerte.id
        resultat["message"] = "Alerte enregistrée."

    else:
        resultat["message"] = "Aucune anomalie détectée."

    # 4️⃣ Retour complet
    resultat["mesure_id"] = mesure.id

    return resultat
