from sqlalchemy.orm import Session
from models.alerte import Alerte


def creer_alerte(db: Session, zone_id: int, capteur_id: int,
                 type_probleme: str, message_resolution: str):
    """
    Crée une alerte dans la table alertes.
    """
    alerte = Alerte(
        zone_id=zone_id,
        capteur_id=capteur_id,
        type_probleme=type_probleme,
        message_resolution=message_resolution
    )

    db.add(alerte)
    db.commit()
    db.refresh(alerte)

    return alerte
