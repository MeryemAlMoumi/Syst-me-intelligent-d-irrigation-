from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.mesure import Mesure
from models.zone import Zone
import schemas

router = APIRouter(prefix="/irrigation", tags=["Irrigation"])

@router.get("/", response_model=schemas.IrrigationResponse)
def get_irrigation_data(db: Session = Depends(get_db)):
    """
    Calcule les stats et l'historique d'irrigation basé sur les mesures où la pompe était active (debit > 0).
    """
    # Récupérer les 50 dernières mesures d'arrosage
    arrosages = db.query(Mesure).filter(Mesure.debit > 0).order_by(Mesure.date_lecture.desc()).limit(50).all()
    
    history = []
    total_vol = 0
    total_gain = 0
    count = 0

    for m in arrosages:
        # Trouver le nom de la zone
        zone_nom = "Inconnue"
        if m.zone_id:
            z = db.query(Zone).filter(Zone.id == m.zone_id).first()
            if z: zone_nom = z.nom

        # Simulation des données calculées (car une mesure est instantanée)
        duree = 30 # minutes estimées par session
        volume = int(m.debit * duree) if m.debit else 0
        h_avant = int(m.humidite - 10) if m.humidite else 40
        h_apres = int(m.humidite) if m.humidite else 50
        gain = h_apres - h_avant

        total_vol += volume
        total_gain += gain
        count += 1

        history.append({
            "id": m.id,
            "zone": zone_nom,
            "date": m.date_lecture,
            "duree": duree,
            "volume": volume,
            "humidite_avant": h_avant,
            "humidite_apres": h_apres,
            "gain": gain
        })

    # Calcul des moyennes globales
    efficacite = int(total_gain / count) if count > 0 else 0
    
    stats = {
        "total_arrosages": count,
        "volume_total": total_vol,
        "efficacite_moyenne": efficacite
    }

    return {"stats": stats, "history": history}