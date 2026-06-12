from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.schemas import EmployeInput


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "modele_lightgbm_attrition.joblib"
)

FREQUENCE_DEPLACEMENT_MAPPING = {
    "Aucun": 0.0,
    "Occasionnel": 1.0,
    "Frequent": 2.0,
}


@lru_cache(maxsize=1)
def charger_modele() -> dict[str, Any]:
    return joblib.load(MODEL_PATH)


def preparer_donnees(employe: EmployeInput) -> pd.DataFrame:
    artefact = charger_modele()
    colonnes_entree = artefact["colonnes_entree"]

    donnees = employe.model_dump()
    donnees["frequence_deplacement"] = FREQUENCE_DEPLACEMENT_MAPPING[
        donnees["frequence_deplacement"]
    ]

    return pd.DataFrame([donnees], columns=colonnes_entree)


def predire_attrition(employe: EmployeInput) -> dict[str, Any]:
    artefact = charger_modele()
    pipeline = artefact["pipeline"]
    seuil = float(artefact["seuil"])

    donnees_modele = preparer_donnees(employe)
    probabilite_depart = float(pipeline.predict_proba(donnees_modele)[0, 1])
    risque_depart = probabilite_depart >= seuil

    return {
        "prediction": "Oui" if risque_depart else "Non",
        "risque_depart": risque_depart,
        "probabilite_depart": round(probabilite_depart, 3),
        "seuil": seuil,
    }