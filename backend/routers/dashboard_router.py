from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.zone import Zone
import schemas

# Création du routeur avec le préfixe /zones
router = APIRouter(prefix="/zones", tags=["Dashboard"])

@router.get("/", response_model=list[schemas.ZoneDisplay])
def get_dashboard_data(db: Session = Depends(get_db)):
    zones = db.query(Zone).all()
    return zones