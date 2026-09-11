import pytest
from fastapi.testclient import TestClient
from src.config import settings

from src.api import app

from tests.conftest import CLE_API_DE_TEST

# Ce client envoie la clé sur TOUTES ses requêtes : les 10 tests existants
# n'ont donc aucune modification à subir.
client = TestClient(app, headers={"X-API-Key": CLE_API_DE_TEST})

# Client volontairement anonyme, pour tester le refus.
client_anonyme = TestClient(app)


def test_racine_repond_ok():
    """Vérifie que l'endpoint racine répond bien avec un statut 200 et 'ok'."""
    reponse = client.get("/")
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "ok"


def test_health_repond_ok():
    """Vérifie que l'endpoint health répond bien avec un statut 200 et 'healthy'."""
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.json()["status"] == "healthy"


def test_model_info_expose_la_structure_attendue():
    """Contrat de l'endpoint : les bonnes cles, les bons types. Independant du modele."""
    reponse = client.get("/model-info")

    assert reponse.status_code == 200

    donnees = reponse.json()
    assert set(donnees) == {"seuil", "nombre_de_features", "etapes_pipeline"}
    assert 0 < donnees["seuil"] < 1
    assert donnees["nombre_de_features"] > 0
    assert isinstance(donnees["etapes_pipeline"], list)


def test_artefact_deploye_est_bien_celui_attendu():
    """Sentinelle : verifie que le .joblib servi est le modele valide au projet 4.

    Ce test DOIT casser si l'artefact est remplace : c'est le signal qu'une
    revalidation du modele est necessaire avant mise en production.
    """
    donnees = client.get("/model-info").json()

    assert donnees["seuil"] == pytest.approx(0.299)
    assert donnees["nombre_de_features"] == 21
    assert donnees["etapes_pipeline"] == ["feature_engineer", "preprocessor", "model"]


def test_predict_repond_ok(employe_valide):
    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 200

    donnees = reponse.json()
    assert donnees["prediction"] in ["Oui", "Non"]
    assert isinstance(donnees["risque_depart"], bool)
    assert 0 <= donnees["probabilite_depart"] <= 1
    assert donnees["seuil"] == pytest.approx(0.299)

def test_predict_rejette_champ_manquant(employe_valide):
    employe_valide.pop("age")

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 422

def test_predict_rejette_valeur_invalide(employe_valide):
    employe_valide["frequence_deplacement"] = "Rare"

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 422

def test_profil_a_risque_score_plus_haut_qu_un_profil_sur(employe_valide, employe_faible_risque):
    """Test de comportement : le modele doit ORDONNER correctement deux profils
    contrastes. Independant du calibrage, il survit a un reentrainement — mais
    il casse si les probabilites sont inversees ou le modele remplace par erreur.
    """
    reponse_risque = client.post("/predict", json=employe_valide)
    reponse_sur = client.post("/predict", json=employe_faible_risque)

    assert reponse_risque.status_code == 200
    assert reponse_sur.status_code == 200

    proba_risque = reponse_risque.json()["probabilite_depart"]
    proba_sur = reponse_sur.json()["probabilite_depart"]

    assert proba_risque > proba_sur

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


# --- Authentification ------------------------------------------------------


def test_predict_sans_cle_est_refuse(employe_valide):
    """Sans en-tête X-API-Key, l'API refuse avant même de charger le modèle."""
    reponse = client_anonyme.post("/predict", json=employe_valide)

    assert reponse.status_code == 401


def test_predict_avec_mauvaise_cle_est_refuse(employe_valide):
    """Une clé qui ne correspond pas est refusée de la même façon."""
    reponse = client.post(
        "/predict",
        json=employe_valide,
        headers={"X-API-Key": "mauvaise-cle"},
    )

    assert reponse.status_code == 401


def test_model_info_est_aussi_protege():
    """La protection ne couvre pas que /predict."""
    assert client_anonyme.get("/model-info").status_code == 401


def test_serveur_sans_cle_configuree_renvoie_500(employe_valide, monkeypatch):
    """Clé absente de la configuration : erreur serveur, pas erreur client."""
    monkeypatch.setattr(settings, "api_key", "")

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 500


class _FakeSessionQuiReussit:
    """Doublure de session qui simule une base qui repond normalement.

    Elle imite les deux moments ou PostgreSQL attribue un identifiant :
    flush() donne son id a l'employe (via la sequence), commit() donne le
    sien a la prediction. Elle memorise aussi ce qu'on lui a demande
    d'ecrire, pour qu'on puisse le verifier.
    """

    def __init__(self):
        self.objets_ajoutes = []

    def add(self, objet):
        self.objets_ajoutes.append(objet)

    def flush(self):
        self.objets_ajoutes[0].id = 42      # l'employe

    def commit(self):
        self.objets_ajoutes[1].id = 99      # la prediction

    def rollback(self):
        pass

    def close(self):
        pass


def test_predict_enregistre_entree_et_sortie_quand_la_base_repond(
    employe_valide, monkeypatch
):
    """Chemin nominal de la persistance : l'entree ET la sortie sont archivees,
    et la prediction enregistree correspond bien a celle renvoyee au client.
    """
    session_factice = _FakeSessionQuiReussit()
    monkeypatch.setattr("src.api.DB_ENABLED", True)
    monkeypatch.setattr("src.api.SessionLocal", lambda: session_factice)

    reponse = client.post("/predict", json=employe_valide)

    assert reponse.status_code == 200
    donnees = reponse.json()
    assert donnees["enregistre"] is True
    assert donnees["id_prediction"] == 99

    # Deux objets ecrits : l'employe (entree) puis la prediction (sortie).
    assert len(session_factice.objets_ajoutes) == 2
    employe_ecrit, prediction_ecrite = session_factice.objets_ajoutes

    # La cle etrangere pointe bien sur l'employe qui vient d'etre cree.
    assert prediction_ecrite.employe_id == employe_ecrit.id

    # Ce qui est archive est exactement ce qui a ete renvoye au client.
    assert prediction_ecrite.probabilite == donnees["probabilite_depart"]
    assert prediction_ecrite.seuil_utilise == donnees["seuil"]