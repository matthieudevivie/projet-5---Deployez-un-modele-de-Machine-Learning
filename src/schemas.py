from typing import Literal
from pydantic import BaseModel, Field

class EmployeInput(BaseModel):
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