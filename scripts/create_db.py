"""Script à lancer une seule fois pour créer les tables dans PostgreSQL.

Usage : uv run python scripts/create_db.py
"""

import sys
from pathlib import Path

# Permet d'importer src/database.py depuis le dossier scripts/
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from database import Base, engine  # noqa: E402


def main() -> None:
    print("Création des tables dans la base...")
    Base.metadata.create_all(bind=engine)
    print("Terminé. Tables créées : employes, predictions.")


if __name__ == "__main__":
    main()