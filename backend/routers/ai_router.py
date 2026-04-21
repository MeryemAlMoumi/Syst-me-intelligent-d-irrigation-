from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.ai_service import analyser_par_ai
from models.mesure import Mesure

router = APIRouter(prefix="/ai", tags=["IA"])

@router.get("/analyse-derniere-mesure")
def analyse_derniere_mesure(db: Session = Depends(get_db)):
    """
    Récupère la dernière mesure de la table Mesure et applique le modèle IA
    """
    # 1️⃣ Récupérer la dernière ligne selon date_lecture ou id
    derniere_mesure = db.query(Mesure).order_by(Mesure.id.desc()).first()

    if not derniere_mesure:
        return {"status": "error", "message": "Aucune mesure trouvée"}

    # 2️⃣ Appliquer IA
    resultat = analyser_par_ai(
        pression=derniere_mesure.pression,
        debit=derniere_mesure.debit,
        humidite=derniere_mesure.humidite
    )

    # 3️⃣ Retourner seulement anomalie et solution
    return {
        "anomalie": resultat["anomalie"],
        "solution": resultat["solution"]
    }
