---
title: API Attrition Projet 5
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Déploiement d’un modèle de Machine Learning - Prédiction d'attrition chez une ESN

## Présentation du projet

Contexte : Futurisys, une entreprise innovante souhaite rendre ses modèles de machine learning opérationnels et accessibles via une API performante.

Objectif : Ce projet a pour but de déployer un modèle de machine learning à l'aide d'outils modernes. J'ai choisi le modèle du projet 4 (Identifiez les causes d'attrition au sein d'une ESN (TechNova Partners), cf. https://openclassrooms.com/fr/paths/1047/projects/3146/4343-mission---partie-1---identifiez-les-causes-d'attrition-au-sein-d'une-esn-). Il s'agit d'une classification supervisée visant à prédire le départ d'un employé (attrition) à partir de ses caractéristiques RH.

## Structure du dépôt

- `data/` contient les fichiers CSV d'exemple utilisés pour entraîner le modèle d'attrition.
- `models/` contient le modèle entraîné exporté au format `.joblib`.
- `notebooks/` contient le notebook complet du projet 4 et le notebook d'export du modèle final.
- `src/` contient le code applicatif de l'API FastAPI.
  - `api.py` définit les endpoints HTTP.
  - `schemas.py` définit les schémas Pydantic de validation des données entrantes.
  - `predictor.py` charge le modèle et exécute les prédictions.
  - `features.py` contient le feature engineering utilisé par le pipeline du modèle.
- `tests/` contient les tests automatisés Pytest.
- `sql/` est prévu pour l'étape PostgreSQL du projet.

## Modèle utilisé

Le modèle retenu est un `LightGBMClassifier` avec feature engineering, optimisation des hyperparamètres avec Optuna et seuil de décision personnalisé.

Le pipeline sauvegardé contient :

1. une étape de feature engineering ;
2. un prétraitement des variables numériques et catégorielles ;
3. le modèle LightGBM entraîné.

Le seuil de décision utilisé est `0.371`.

Le modèle est exporté dans : models/modele_lightgbm_attrition.joblib
Le notebook permettant de reconstruire cet export est : notebooks/modele_lightgbm_export.ipynb

## Pré-requis

- Python 3.14
- uv

## Instructions d'installation

```bash
git clone https://github.com/matthieu3344/projet-5---Deployez-un-modele-de-Machine-Learning
cd projet-5---Deployez-un-modele-de-Machine-Learning
uv sync
```

## Lancer l'API en local

uv run fastapi dev src/api.py
L'API est ensuite disponible à l'adresse : http://127.0.0.1:8000
La documentation Swagger est disponible ici : http://127.0.0.1:8000/docs

## Endpoints disponibles

GET /
Vérifie que l'API répond.

Exemple de réponse :
{
  "message": "L'API est en ligne",
  "statut": "ok"
}

GET /health
Endpoint de santé utilisé pour vérifier que le service est disponible.

Exemple de réponse :
{
  "status": "healthy"
}

POST /predict
Retourne une prédiction d'attrition pour un employé.

Exemple de requête :
{
  "satisfaction_employee_environnement": 2,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 1,
  "satisfaction_employee_equilibre_pro_perso": 1,
  "note_evaluation_precedente": 3,
  "note_evaluation_actuelle": 3,
  "heure_supplementaires": "Oui",
  "age": 41,
  "genre": "F",
  "revenu_mensuel": 5993,
  "statut_marital": "Célibataire",
  "poste": "Cadre Commercial",
  "nombre_experiences_precedentes": 8,
  "annees_dans_l_entreprise": 6,
  "nombre_participation_pee": 0,
  "nb_formations_suivies": 0,
  "distance_domicile_travail": 1,
  "niveau_education": 2,
  "domaine_etude": "Infra & Cloud",
  "frequence_deplacement": "Occasionnel",
  "annees_depuis_la_derniere_promotion": 0
}

Exemple de réponse :
{
  "prediction": "Oui",
  "risque_depart": true,
  "probabilite_depart": 0.858,
  "seuil": 0.371
}

Les données entrantes sont validées avec Pydantic. Par exemple, une valeur invalide pour frequence_deplacement ou un âge inférieur à 18 ans renvoie une erreur 422.

## Tests

Lancer les tests :
uv run pytest

Lancer le contrôle de style :
uv run ruff check src tests

## CI/CD

Le projet utilise GitHub Actions pour lancer les tests automatiquement lors des push et pull requests.
Le déploiement continu vers Hugging Face Spaces est configuré via le workflow dédié.

## Authentification

L'API ne met pas encore en place d'authentification applicative. Cette partie pourra être renforcée dans une étape ultérieure selon les besoins de sécurisation.

## Sécurisation
Les secrets, comme les tokens Hugging Face ou les futurs accès PostgreSQL, ne sont pas commités dans le dépôt.
Ils doivent être fournis via :
un fichier .env en local ;
les secrets GitHub Actions ;
les variables d'environnement de la plateforme de déploiement.

## Gestion Git

Le développement se fait avec des branches dédiées par fonctionnalité, par exemple : git switch -c feature/api-prediction
Une fois la fonctionnalité terminée, elle est intégrée à main via une pull request.