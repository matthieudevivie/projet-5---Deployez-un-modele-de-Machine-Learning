"""Tests unitaires du predicteur (src/predictor.py).

On teste ici la fonction PURE decision_depuis_proba : elle ne fait que
traduire une probabilite + un seuil en decision metier. Aucun modele a
charger, donc des tests rapides et 100 % deterministes.
"""

from src.predictor import decision_depuis_proba


def test_proba_au_dessus_du_seuil_predit_oui():
    """Une proba clairement au-dessus du seuil doit donner 'Oui'."""
    resultat = decision_depuis_proba(0.9, 0.37)

    assert resultat["prediction"] == "Oui"
    assert resultat["risque_depart"] is True


def test_proba_sous_le_seuil_predit_non():
    """Une proba clairement sous le seuil doit donner 'Non'."""
    resultat = decision_depuis_proba(0.1, 0.37)

    assert resultat["prediction"] == "Non"
    assert resultat["risque_depart"] is False


def test_proba_egale_au_seuil_predit_oui():
    """Cas limite : proba == seuil. Le code utilise '>=', donc 'Oui'."""
    resultat = decision_depuis_proba(0.37, 0.37)

    assert resultat["prediction"] == "Oui"
    assert resultat["risque_depart"] is True
