from typing import Literal
from pydantic import BaseModel, Field

class EmployeInput(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "satisfaction_employee_environnement": 2,
                    "satisfaction_employee_nature_travail": 4,
                    "satisfaction_employee_equipe": 1,
                    "satisfaction_employee_equilibre_pro_perso": 1,
                    "note_evaluation_precedente": 3,
                    "note_evaluation_actuelle": 3,
                    "heure_supplementaires": "Oui",
                    "age": 41,
                    "genre": "F",
                    "revenu_mensuel": 5993,
                    "statut_marital": "Célibataire",
                    "poste": "Cadre Commercial",
                    "nombre_experiences_precedentes": 8,
                    "annees_dans_l_entreprise": 6,
                    "nombre_participation_pee": 0,
                    "nb_formations_suivies": 0,
                    "distance_domicile_travail": 1,
                    "niveau_education": 2,
                    "domaine_etude": "Infra & Cloud",
                    "frequence_deplacement": "Occasionnel",
                    "annees_depuis_la_derniere_promotion": 0,
                }
            ]
        }
    }

    satisfaction_employee_environnement: int = Field(..., ge=1, le=4)
    satisfaction_employee_nature_travail: int = Field(..., ge=1, le=4)
    satisfaction_employee_equipe: int = Field(..., ge=1, le=4)
    satisfaction_employee_equilibre_pro_perso: int = Field(..., ge=1, le=4)
    note_evaluation_precedente: int = Field(..., ge=1, le=4)
    note_evaluation_actuelle: int = Field(..., ge=1, le=4)

    heure_supplementaires: Literal["Oui", "Non"]
    age: int = Field(..., ge=18, le=70)
    genre: Literal["F", "M"]
    revenu_mensuel: int = Field(..., ge=0)
    statut_marital: Literal["Célibataire", "Divorcé(e)", "Marié(e)"]
    poste: str

    nombre_experiences_precedentes: int = Field(..., ge=0)
    annees_dans_l_entreprise: int = Field(..., ge=0)
    nombre_participation_pee: int = Field(..., ge=0)
    nb_formations_suivies: int = Field(..., ge=0)
    distance_domicile_travail: int = Field(..., ge=0)

    niveau_education: int = Field(..., ge=1, le=5)
    domaine_etude: str
    frequence_deplacement: Literal["Aucun", "Occasionnel", "Frequent"]
    annees_depuis_la_derniere_promotion: int = Field(..., ge=0)


class PredictionOutput(BaseModel):
    prediction: Literal["Oui", "Non"]
    risque_depart: bool
    probabilite_depart: float = Field(..., ge=0, le=1)
    seuil: float = Field(..., ge=0, le=1)
    enregistre: bool
    id_prediction: int | None