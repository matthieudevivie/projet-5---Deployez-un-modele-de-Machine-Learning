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


@pytest.mark.parametrize(
    "champ, valeur",
    [
        ("age", 17),
        ("age", 71),
        ("satisfaction_employee_environnement", 0),
        ("satisfaction_employee_environnement", 5),
        ("satisfaction_employee_nature_travail", 0),
        ("satisfaction_employee_nature_travail", 5),
        ("frequence_deplacement", "Rare"),        # modalite non autorisee
        ("statut_marital", "Pacsé(e)"),           # idem, sur un autre champ
    ],
)
def test_valeur_invalide_est_rejetee(employe_valide, champ, valeur):
    """Bornes numeriques (ge/le) et modalites autorisees (Literal) : tout ecart
    doit lever une ValidationError a la construction de l'objet."""
    employe_valide[champ] = valeur

    with pytest.raises(ValidationError):
        EmployeInput(**employe_valide)


def test_champ_obligatoire_manquant_est_rejete(employe_valide):
    """Retirer un champ obligatoire (age) doit lever une ValidationError."""
    del employe_valide["age"]

    with pytest.raises(ValidationError):
        EmployeInput(**employe_valide)
