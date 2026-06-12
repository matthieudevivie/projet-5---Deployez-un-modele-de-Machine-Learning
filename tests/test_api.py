import pytest
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_racine_repond_ok():
    """Vérifie que l'endpoint racine répond bien avec un statut 200 et 'ok'."""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "ok"


def employe_valide():
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

def test_predict_repond_ok():
    reponse = client.post("/predict", json=employe_valide())

    assert reponse.status_code == 200

    donnees = reponse.json()
    assert donnees["prediction"] in ["Oui", "Non"]
    assert isinstance(donnees["risque_depart"], bool)
    assert 0 <= donnees["probabilite_depart"] <= 1
    assert donnees["seuil"] == pytest.approx(0.371)

def test_predict_rejette_champ_manquant():
    payload = employe_valide()
    payload.pop("age")

    reponse = client.post("/predict", json=payload)

    assert reponse.status_code == 422

def test_predict_rejette_valeur_invalide():
    payload = employe_valide()
    payload["frequence_deplacement"] = "Rare"

    reponse = client.post("/predict", json=payload)

    assert reponse.status_code == 422