import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Import de la base de données
from database import SessionLocal, engine, Base

# Import des modèles (Assurez-vous que vos fichiers sont bien dans un dossier 'models')
from models.plante import Plante
from models.zone import Zone
from models.capteur import Capteur
from models.mesure import Mesure
from models.alerte import Alerte
# Si vous avez un modèle Meteo, vous pouvez aussi l'importer, sinon on laisse vide
# from models.meteo import Meteo 

def seed_data():
    print("🌱 Initialisation de la base de données...")
    
    # 1. On vide les tables existantes pour éviter les doublons (Ordre important à cause des clés étrangères)
    # On recrée tout proprement
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    try:
        print("🌱 Création des Plantes...")
        tomate = Plante(nom="Tomates", besoin_eau_mm_jour=5.0)
        carotte = Plante(nom="Carottes", besoin_eau_mm_jour=4.0)
        laitue = Plante(nom="Laitues", besoin_eau_mm_jour=3.0)
        db.add_all([tomate, carotte, laitue])
        db.commit()

        print("🌱 Création des Zones...")
        # On lie les zones aux plantes créées
        z_nord = Zone(nom="Zone Nord", plante_id=tomate.id)
        z_est = Zone(nom="Zone Est", plante_id=carotte.id)
        z_sud = Zone(nom="Zone Sud", plante_id=laitue.id)
        db.add_all([z_nord, z_est, z_sud])
        db.commit()

        print("🌱 Création des Capteurs...")
        # Capteurs pour Zone Nord
        c_hum_n = Capteur(nom="Capteur Sol Nord", type_capteur="Humidité", zone_id=z_nord.id)
        c_deb_n = Capteur(nom="Débitmètre Nord", type_capteur="Débit", zone_id=z_nord.id)
        
        # Capteurs pour Zone Est
        c_hum_e = Capteur(nom="Capteur Sol Est", type_capteur="Humidité", zone_id=z_est.id)
        
        # Capteurs pour Zone Sud
        c_hum_s = Capteur(nom="Capteur Sol Sud", type_capteur="Humidité", zone_id=z_sud.id)

        db.add_all([c_hum_n, c_deb_n, c_hum_e, c_hum_s])
        db.commit()

        print("🌱 Génération de l'Historique des Mesures (48h)...")
        # On génère des données pour les dernières 48 heures
        maintenant = datetime.now()
        mesures = []

        for i in range(48):
            temps = maintenant - timedelta(hours=i)
            
            # --- Zone Nord (Tomates) : Tout va bien ---
            # Humidité varie entre 60% et 80% (cycle jour/nuit simulé)
            hum_n = 70 + random.uniform(-10, 10) 
            mesures.append(Mesure(
                capteur_id=c_hum_n.id, zone_id=z_nord.id,
                humidite=hum_n, temperature=22 + random.uniform(-5, 5),
                pression=2.5, debit=0, date_lecture=temps
            ))

            # --- Zone Est (Carottes) : Un peu sec ---
            # Humidité basse (30-45%)
            hum_e = 40 + random.uniform(-5, 5)
            mesures.append(Mesure(
                capteur_id=c_hum_e.id, zone_id=z_est.id,
                humidite=hum_e, temperature=24 + random.uniform(-5, 5),
                pression=2.2, debit=0, date_lecture=temps
            ))

            # --- Simulation d'un arrosage sur Zone Nord il y a 5h ---
            if i == 5:
                # On ajoute une mesure avec du débit
                mesures.append(Mesure(
                    capteur_id=c_deb_n.id, zone_id=z_nord.id,
                    humidite=hum_n, temperature=22,
                    pression=2.8, debit=120.0, date_lecture=temps
                ))

        db.add_all(mesures)
        db.commit()

        print("🌱 Création des Alertes...")
        # Une alerte en cours (Zone Est trop sèche)
        a1 = Alerte(
            zone_id=z_est.id,
            capteur_id=c_hum_e.id,
            type_probleme="Sécheresse critique",
            message_resolution="Arrosage manuel recommandé immédiatement. Vérifier vanne.",
            date_alerte=maintenant - timedelta(hours=2)
        )
        
        # Une alerte résolue (Zone Sud)
        a2 = Alerte(
            zone_id=z_sud.id,
            capteur_id=c_hum_s.id,
            type_probleme="Fuite détectée",
            message_resolution="Remplacement du joint effectué.",
            date_alerte=maintenant - timedelta(days=2)
            # Si vous avez ajouté une colonne 'statut' ou 'resolu' dans le modèle Alerte, mettez-le ici
            # Sinon, on suppose que c'est géré autrement ou on le laisse tel quel.
        )
        # Pour cet exemple, on suppose que le modèle a les champs par défaut
        
        db.add_all([a1, a2])
        db.commit()

        print("✅ Base de données remplie avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors du remplissage : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()