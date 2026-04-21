# service_mesure.py
from sqlalchemy.orm import Session
from models.mesure import Mesure

def enregistrer_mesure(db: Session, capteur_id: int, zone_id: int,
                       pression: float, debit: float, humidite: float,
                       temperature: float = None) -> Mesure:
    """
    Enregistre une mesure dans la base de données.
    """
    mesure = Mesure(
        capteur_id=capteur_id,
        zone_id=zone_id,
        pression=pression,
        debit=debit,
        humidite=humidite,
        temperature=temperature
    )
    db.add(mesure)
    db.commit()
    db.refresh(mesure)
    return mesure
