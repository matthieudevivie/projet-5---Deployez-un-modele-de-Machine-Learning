import pytest
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_racine_repond_ok():
    """Vérifie que l'endpoint racine répond bien avec un statut 200 et 'ok'."""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "ok"


def test_predict_repond_ok(employe_valide):
    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 200

    donnees = reponse.json()
    assert donnees["prediction"] in ["Oui", "Non"]
    assert isinstance(donnees["risque_depart"], bool)
    assert 0 <= donnees["probabilite_depart"] <= 1
    assert donnees["seuil"] == pytest.approx(0.371)

def test_predict_rejette_champ_manquant(employe_valide):
    employe_valide.pop("age")

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 422

def test_predict_rejette_valeur_invalide(employe_valide):
    employe_valide["frequence_deplacement"] = "Rare"

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 422


# --- Degradation gracieuse de la base (tests avec mocking) ----------------


class _FakeSessionQuiEchoue:
    """Doublure de session qui simule une base en panne : add() leve une erreur.

    rollback() et close() sont des coquilles vides : on veut juste que le code
    de gestion d'erreur (except/finally) puisse les appeler sans planter.
    """

    def add(self, objet):
        raise RuntimeError("Base de donnees injoignable (simulee)")

    def rollback(self):
        pass

    def close(self):
        pass


def test_predict_ignore_enregistrement_si_base_desactivee(employe_valide, monkeypatch):
    """Base desactivee (cas Hugging Face) : la prediction passe, sans enregistrement."""
    monkeypatch.setattr("src.api.DB_ENABLED", False)

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 200
    donnees = reponse.json()
    assert donnees["prediction"] in ["Oui", "Non"]
    assert donnees["enregistre"] is False
    assert donnees["id_prediction"] is None


def test_predict_fonctionne_meme_si_base_echoue(employe_valide, monkeypatch):
    """Base active mais EN PANNE : la prediction passe quand meme (degradation)."""
    # 1) on active la base...
    monkeypatch.setattr("src.api.DB_ENABLED", True)
    # 2) ...mais on la remplace par une doublure qui echoue a la moindre ecriture.
    monkeypatch.setattr("src.api.SessionLocal", lambda: _FakeSessionQuiEchoue())

    reponse = client.post("/predict", json=employe_valide)

    # La promesse : l'incident base est INVISIBLE pour le client.
    assert reponse.status_code == 200
    donnees = reponse.json()
    assert donnees["prediction"] in ["Oui", "Non"]
    assert donnees["enregistre"] is False
    assert donnees["id_prediction"] is None