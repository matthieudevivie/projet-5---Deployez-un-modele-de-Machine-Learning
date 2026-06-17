"""Script d'interrogation de la base via SQLAlchemy.

Montre comment lire les données tracées (employés + prédictions) depuis Python.

Usage : uv run python scripts/interroger.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from database import Employe, Prediction, SessionLocal  # noqa: E402


def historique_employe(session, employe_id: int) -> list[Prediction]:
    """Renvoie toutes les prédictions d'un employé, de la plus récente à la plus ancienne."""
    return (
        session.query(Prediction)
        .filter(Prediction.employe_id == employe_id)
        .order_by(Prediction.date_prediction.desc())
        .all()
    )


def taux_de_bonnes_predictions(session) -> dict:
    """Compare prédiction et réalité pour mesurer la performance en production.

    On ignore les employés dont la réalité est inconnue (cible NULL).
    """
    lignes = (
        session.query(Prediction, Employe)
        .join(Employe, Employe.id == Prediction.employe_id)
        .filter(Employe.a_quitte_l_entreprise.isnot(None))
        .all()
    )

    total = len(lignes)
    corrects = 0
    for prediction, employe in lignes:
        reel_part = employe.a_quitte_l_entreprise == 1
        if prediction.attrition_predite == reel_part:
            corrects += 1

    taux = round(100.0 * corrects / total, 1) if total else 0.0
    return {"total": total, "corrects": corrects, "taux_pct": taux}


def employes_a_risque(session, limite: int = 10) -> list[tuple]:
    """Liste les profils prédits à risque, triés par probabilité décroissante."""
    return (
        session.query(Employe.id, Employe.poste, Prediction.probabilite)
        .join(Prediction, Employe.id == Prediction.employe_id)
        .filter(Prediction.attrition_predite.is_(True))
        .order_by(Prediction.probabilite.desc())
        .limit(limite)
        .all()
    )


def main() -> None:
    session = SessionLocal()
    try:
        perf = taux_de_bonnes_predictions(session)
        print(
            f"Performance : {perf['corrects']}/{perf['total']} predictions correctes "
            f"({perf['taux_pct']} %)"
        )

        print("\nTop employes a risque :")
        for employe_id, poste, proba in employes_a_risque(session, limite=5):
            print(f"  Employe {employe_id:>4} | {poste:<25} | proba {proba}")
    finally:
        session.close()


if __name__ == "__main__":
    main()