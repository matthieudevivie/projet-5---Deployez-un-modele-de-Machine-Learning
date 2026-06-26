"""Tests unitaires du feature engineering (src/features.py).

FeatureEngineer est un transformer scikit-learn en deux phases :
  - fit(X)       : apprend les medianes de revenu (par poste, par education) ;
  - transform(X) : fabrique les features derivees a partir de ces medianes.

On entraine le transformer sur un mini-jeu MAITRISE (medianes connues
d'avance), puis on verifie que chaque feature correspond a sa formule metier.
"""

import pandas as pd
import pytest

from src.features import FeatureEngineer


def _ligne(**overrides):
    """Un employe par defaut ; chaque test ne surcharge que ce qui l'interesse."""
    base = {
        "age": 40,
        "revenu_mensuel": 5000,
        "annees_dans_l_entreprise": 5,
        "nombre_participation_pee": 2,
        "annees_depuis_la_derniere_promotion": 1,
        "poste": "Cadre Commercial",
        "niveau_education": 3,
        "satisfaction_employee_environnement": 2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
    }
    base.update(overrides)
    return base


@pytest.fixture
def transformer():
    """Un FeatureEngineer DEJA entraine (fixture locale a ce fichier).

    Medianes de revenu apprises par fit() :
      - 'Cadre Commercial' : mediane(4000, 6000) = 5000
      - 'Technicien'       : mediane(3000)       = 3000
    """
    donnees_fit = pd.DataFrame(
        [
            _ligne(poste="Cadre Commercial", revenu_mensuel=4000),
            _ligne(poste="Cadre Commercial", revenu_mensuel=6000),
            _ligne(poste="Technicien", revenu_mensuel=3000),
        ]
    )
    return FeatureEngineer().fit(donnees_fit)


# --- fit : la phase d'apprentissage --------------------------------------

def test_fit_apprend_les_medianes_par_poste(transformer):
    """fit() doit memoriser la bonne mediane de revenu pour chaque poste."""
    assert transformer.mediane_par_poste_["Cadre Commercial"] == 5000
    assert transformer.mediane_par_poste_["Technicien"] == 3000


# --- transform : la phase d'application ----------------------------------

def test_transform_cree_toutes_les_colonnes_attendues(transformer):
    """transform() doit ajouter toutes les features derivees."""
    resultat = transformer.transform(pd.DataFrame([_ligne()]))

    colonnes_attendues = [
        "jeune",
        "bas_revenu",
        "premiere_annee",
        "sans_pee",
        "jeune_et_premiere_annee",
        "satisfaction_globale",
        "ratio_stagnation",
        "ratio_salaire_mediane_poste",
        "ratio_salaire_mediane_education",
    ]
    for colonne in colonnes_attendues:
        assert colonne in resultat.columns


def test_indicateur_jeune(transformer):
    """'jeune' vaut 1 si age < 33, sinon 0 (cas limite teste des deux cotes)."""
    jeune = transformer.transform(pd.DataFrame([_ligne(age=25)]))
    senior = transformer.transform(pd.DataFrame([_ligne(age=40)]))

    assert jeune["jeune"].iloc[0] == 1
    assert senior["jeune"].iloc[0] == 0


def test_indicateur_bas_revenu(transformer):
    """'bas_revenu' vaut 1 si revenu < 3000."""
    bas = transformer.transform(pd.DataFrame([_ligne(revenu_mensuel=2000)]))
    haut = transformer.transform(pd.DataFrame([_ligne(revenu_mensuel=5000)]))

    assert bas["bas_revenu"].iloc[0] == 1
    assert haut["bas_revenu"].iloc[0] == 0


def test_satisfaction_globale_est_la_moyenne(transformer):
    """satisfaction_globale = moyenne des 4 notes de satisfaction."""
    df = pd.DataFrame(
        [
            _ligne(
                satisfaction_employee_environnement=2,
                satisfaction_employee_nature_travail=4,
                satisfaction_employee_equipe=1,
                satisfaction_employee_equilibre_pro_perso=1,
            )
        ]
    )  # (2 + 4 + 1 + 1) / 4 = 2.0
    resultat = transformer.transform(df)

    assert resultat["satisfaction_globale"].iloc[0] == pytest.approx(2.0)


def test_ratio_salaire_mediane_poste(transformer):
    """Un employe paye exactement a la mediane de son poste a un ratio de 1.0."""
    # Mediane apprise pour 'Cadre Commercial' = 5000 ; revenu = 5000 -> ratio 1.0
    df = pd.DataFrame([_ligne(poste="Cadre Commercial", revenu_mensuel=5000)])
    resultat = transformer.transform(df)

    assert resultat["ratio_salaire_mediane_poste"].iloc[0] == pytest.approx(1.0)


def test_transform_ne_modifie_pas_le_dataframe_dentree(transformer):
    """transform() fait X.copy() : le DataFrame d'origine ne doit pas etre altere."""
    df = pd.DataFrame([_ligne()])
    colonnes_avant = df.columns.tolist()

    transformer.transform(df)

    assert df.columns.tolist() == colonnes_avant
