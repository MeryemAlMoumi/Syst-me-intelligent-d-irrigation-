# routers/alertes_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Imports de base et DB
from database import get_db
import schemas

# Imports des modèles
from models.alerte import Alerte
from models.zone import Zone
from models.capteur import Capteur

# Imports des services (IA et Création)
from services.ai_service import analyser_par_ai
from services.alerte_service import creer_alerte

# Création du routeur
router = APIRouter(prefix="/alertes", tags=["Alertes"])

# =====================================================================
# 1️⃣ ROUTE DE LECTURE (GET) - Pour le tableau React
# =====================================================================
@router.get("/", response_model=List[schemas.AlerteDisplay])
def get_alertes_history(db: Session = Depends(get_db)):
    """
    Récupère toutes les alertes enregistrées en base, triées par date (la plus récente en premier).
    """
    alertes = db.query(Alerte).order_by(Alerte.date_alerte.desc()).all()
    
    result = []
    for a in alertes:
        # On récupère le nom de la Zone via l'ID stocké dans l'alerte
        zone_obj = db.query(Zone).filter(Zone.id == a.zone_id).first()
        nom_zone = zone_obj.nom if zone_obj else "Zone inconnue"

        # On récupère le nom du Capteur via l'ID
        capteur_obj = db.query(Capteur).filter(Capteur.id == a.capteur_id).first()
        nom_capteur = capteur_obj.nom if capteur_obj else "Capteur Global"
        
        # 🟢 CORRECTION DE L'ERREUR : On calcule la sévérité
        # On ne lit plus a.severite car elle n'existe pas dans le modèle
        if a.type_probleme in ["fuite", "pompe_defaillante", "Sécheresse critique"]:
            sev_calculee = "haute"
        else:
            sev_calculee = "moyenne"

        # On suppose que le statut est "résolu" si le message de résolution le mentionne
        statut_calcule = "resolu" if "Résolu" in (a.message_resolution or "") else "en_cours"


        # Construction de l'objet pour le Frontend
        result.append({
            "id": a.id,
            "date": a.date_alerte,
            "zone": nom_zone,
            "capteur": nom_capteur,
            "severite": sev_calculee, # On utilise la valeur calculée
            "solution": a.message_resolution if a.message_resolution else "Vérification requise",
            "statut": statut_calcule
        })
        
    return result

# =====================================================================
# 2️⃣ ROUTE D'ANALYSE (POST) - Reste inchangée
# =====================================================================
@router.post("/analyse-et-enregistrer")
def analyser_et_enregistrer(data: dict, db: Session = Depends(get_db)):
    """
    Reçoit des données, utilise l'IA pour détecter une anomalie et enregistre une alerte.
    """
    pression = data.get("pression")
    debit = data.get("debit")
    humidite = data.get("humidite")
    zone_id = data.get("zone_id")
    capteur_id = data.get("capteur_id")

    # 1. Appel au service IA
    resultat_ia = analyser_par_ai(pression, debit, humidite)
    type_anomalie = resultat_ia["anomalie"]
    solution_ia = resultat_ia["solution"]

    message = "Analyse terminée."
    alerte_creee = None

    # 2. Si ce n'est pas "normal", on crée une alerte en BDD
    if type_anomalie != "normal" and type_anomalie != "inconnu":
        # On définit une sévérité simple
        severite_calc = "haute" if type_anomalie in ["fuite", "pompe_defaillante"] else "moyenne"

        nouvelle_alerte = Alerte(
            zone_id=zone_id,
            capteur_id=capteur_id,
            type_probleme=type_anomalie,
            # severite=severite_calc,  <-- On ne stocke pas 'severite' car la colonne n'existe pas
            message_resolution=solution_ia
        )
        db.add(nouvelle_alerte)
        db.commit()
        db.refresh(nouvelle_alerte)
        
        alerte_creee = nouvelle_alerte.id
        message = f"⚠️ Anomalie détectée ({type_anomalie}). Alerte #{alerte_creee} créée."
    else:
        message = "✅ Système normal. Aucune alerte créée."

    return {
        "analyse": resultat_ia,
        "message": message,
        "alerte_id": alerte_creee
    }