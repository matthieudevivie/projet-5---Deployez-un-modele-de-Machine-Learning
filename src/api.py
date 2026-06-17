import logging

from fastapi import FastAPI

from src.database import DB_ENABLED, Employe, Prediction, SessionLocal
from src.predictor import predire_attrition
from src.schemas import EmployeInput

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="API Attrition - Projet 5")


@app.get("/")
def racine():
    """Endpoint racine : prouve simplement que l'API est vivante."""
    return {"message": "L'API est en ligne", "statut": "ok"}


@app.get("/health")
def health():
    """Endpoint de santé : utilisé pour vérifier que le service répond."""
    return {"status": "healthy"}


def enregistrer_en_base(employe: EmployeInput, resultat: dict) -> int | None:
    """Enregistre l'input et l'output en base. Renvoie l'id de prediction, ou None.

    Si la base est desactivee ou injoignable, on n'interrompt PAS la prediction :
    on journalise l'incident et on renvoie None (degradation gracieuse).
    """
    if not DB_ENABLED:
        return None

    session = SessionLocal()
    try:
        employe_en_base = Employe(**employe.model_dump())
        session.add(employe_en_base)
        session.flush()  # force l'attribution de l'id

        prediction_en_base = Prediction(
            employe_id=employe_en_base.id,
            attrition_predite=resultat["risque_depart"],
            probabilite=resultat["probabilite_depart"],
            seuil_utilise=resultat["seuil"],
        )
        session.add(prediction_en_base)
        session.commit()
        return prediction_en_base.id
    except Exception as exc:
        session.rollback()
        logger.warning("Enregistrement en base impossible : %s", exc)
        return None
    finally:
        session.close()


@app.post("/predict")
def predict(employe: EmployeInput):
    # La prediction passe TOUJOURS, independamment de la base.
    resultat = predire_attrition(employe)

    # Enregistrement best-effort : ne fait jamais echouer la requete.
    id_prediction = enregistrer_en_base(employe, resultat)

    resultat["enregistre"] = id_prediction is not None
    resultat["id_prediction"] = id_prediction
    return resultat