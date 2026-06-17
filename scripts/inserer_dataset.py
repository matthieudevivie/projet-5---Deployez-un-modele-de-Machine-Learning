"""Script à lancer une fois pour insérer le dataset dans la table employes.

Usage : uv run python scripts/inserer_dataset.py
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

# Permet d'importer src/database.py depuis le dossier scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from database import Employe, SessionLocal  # noqa: E402

CSV_PATH = PROJECT_ROOT / "data" / "dataset_final.csv"


def inserer_employes() -> None:
    # 1. Lecture du CSV produit par le notebook
    df = pd.read_csv(CSV_PATH)
    print(f"{len(df)} lignes lues depuis {CSV_PATH.name}")

    # 2. Renommage de la colonne id_employe -> id (nom attendu par la table)
    df = df.rename(columns={"id_employe": "id"})

    # 3. Ouverture d'une session (une conversation avec la base)
    session = SessionLocal()
    try:
        # On repart d'une table propre pour pouvoir relancer sans doublon
        session.query(Employe).delete()

        # 4. Transformation de chaque ligne du DataFrame en objet Employe
        #    df.to_dict("records") donne une liste de dictionnaires
        #    [{'id': 1, 'age': 42, ...}, ...]
        for ligne in df.to_dict("records"):
            employe = Employe(**ligne)
            session.add(employe)

        # 5. Validation : c'est ICI que l'écriture en base a réellement lieu
        session.commit()
        print(f"{len(df)} employés insérés avec succès.")

        # 6. Resynchroniser la séquence d'auto-incrémentation de PostgreSQL.
        #    Sans ça, après insertion d'ids explicites, le compteur reste à 1
        #    et les nouveaux employés (via l'API) entreraient en collision.
        #    On le recale sur le plus grand id existant.
        session.execute(
            text(
                "SELECT setval("
                "pg_get_serial_sequence('employes', 'id'), "
                "(SELECT MAX(id) FROM employes))"
            )
        )
        session.commit()
        print("Séquence d'auto-incrémentation resynchronisée.")
    except Exception:
        # En cas d'erreur, on annule tout pour ne pas laisser la base à moitié remplie
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    inserer_employes()