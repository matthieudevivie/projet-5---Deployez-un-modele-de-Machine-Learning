"""Tests unitaires du schema de validation (src/schemas.py).

Pydantic valide les donnees AU MOMENT de construire l'objet EmployeInput.
Si une regle est violee, il leve une ValidationError. On teste donc :
  - qu'une entree valide est acceptee (happy path) ;
  - qu'une entree invalide est bien REJETEE (unhappy path), via pytest.raises.
"""

import pytest
from pydantic import ValidationError

from src.schemas import EmployeInput


def test_employe_valide_est_accepte(employe_valide):
    """Le cas nominal : une entree conforme construit l'objet sans erreur."""
    employe = EmployeInput(**employe_valide)

    assert employe.age == 41
    assert employe.frequence_deplacement == "Occasionnel"


def test_age_hors_bornes_est_rejete(employe_valide):
    """age doit etre entre 18 et 70 ; 10 est trop jeune => ValidationError."""
    employe_valide["age"] = 10

    with pytest.raises(ValidationError):
        EmployeInput(**employe_valide)


def test_valeur_litterale_invalide_est_rejetee(employe_valide):
    """'Rare' n'est pas une frequence_deplacement autorisee => ValidationError."""
    employe_valide["frequence_deplacement"] = "Rare"

    with pytest.raises(ValidationError):
        EmployeInput(**employe_valide)


def test_champ_obligatoire_manquant_est_rejete(employe_valide):
    """Retirer un champ obligatoire (age) doit lever une ValidationError."""
    del employe_valide["age"]

    with pytest.raises(ValidationError):
        EmployeInput(**employe_valide)
