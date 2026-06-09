from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_racine_repond_ok():
    """Vérifie que l'endpoint racine répond bien avec un statut 200 et 'ok'."""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "ok"