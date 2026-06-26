"""Fixtures partagees par tous les tests (pytest detecte ce fichier tout seul).

Pas besoin d'importer ce module : toute fonction decoree @pytest.fixture ici
est disponible dans n'importe quel test, simplement en la nommant en parametre.
"""

import pytest


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
