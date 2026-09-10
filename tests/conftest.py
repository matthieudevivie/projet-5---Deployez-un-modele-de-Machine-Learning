"""Fixtures partagees par tous les tests (pytest detecte ce fichier tout seul).

Pas besoin d'importer ce module : toute fonction decoree @pytest.fixture ici
est disponible dans n'importe quel test, simplement en la nommant en parametre.
"""

import pytest
from src.config import settings

CLE_API_DE_TEST = "cle-de-test-projet5"


@pytest.fixture(autouse=True)
def cle_api_configuree(monkeypatch):
    """Fixe une clé d'API connue pour toute la suite de tests.

    autouse=True : s'applique partout. monkeypatch remet automatiquement
    la valeur d'origine après chaque test.
    """
    monkeypatch.setattr(settings, "api_key", CLE_API_DE_TEST)


@pytest.fixture(autouse=True)
def base_desactivee_par_defaut(monkeypatch):
    """Aucun test n'ecrit dans la vraie base.

    autouse=True : cette fixture s'applique a TOUS les tests sans qu'ils aient
    a la demander. Les deux tests qui exercent la persistance la reactivent
    explicitement avec leur propre monkeypatch, qui s'applique apres celui-ci.
    """
    monkeypatch.setattr("src.api.DB_ENABLED", False)


@pytest.fixture
def employe_valide():
    """Un employe parfaitement conforme au schema EmployeInput.

    pytest reconstruit ce dictionnaire A NEUF pour chaque test : un test peut
    donc le modifier librement sans impacter les autres (isolation).
    """
    return {
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

@pytest.fixture
def employe_faible_risque():
    """Un employe à faible risque de départ
    parfaitement conforme au schema EmployeInput.

    pytest reconstruit ce dictionnaire A NEUF pour chaque test : un test peut
    donc le modifier librement sans impacter les autres (isolation).
    """
    return {
        "satisfaction_employee_environnement": 4,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 4,
        "note_evaluation_precedente": 4,
        "note_evaluation_actuelle": 4,
        "heure_supplementaires": "Non",
        "age": 41,
        "genre": "F",
        "revenu_mensuel": 5993,
        "statut_marital": "Célibataire",
        "poste": "Consultant",
        "nombre_experiences_precedentes": 2,
        "annees_dans_l_entreprise": 6,
        "nombre_participation_pee": 2,
        "nb_formations_suivies": 2,
        "distance_domicile_travail": 1,
        "niveau_education": 4,
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Occasionnel",
        "annees_depuis_la_derniere_promotion": 2,
    }