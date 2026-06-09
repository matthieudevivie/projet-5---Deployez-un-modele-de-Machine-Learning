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

- data/ contient les 3 fichiers de données employé TechNova Partners, ayant permis d'entrainer le modèle de prédiction
- models/ destiné à contenir le modèle entrainé sélectionné dans le projet 4 (LightGBM avec feature engineering, fine-tuné avec Optuna)
- notebooks/ destiné à contenir les différents notebooks (le complet du projet 4 déjà présent, avec analyses, et celui 'épuré' permettant d'entrainer le modèle de prédiction sélectionné, à venir)
- sql/ destiné à contenir le code permettant de migrer l'étape de préparation des données du projet 4 en SQL
- src/ permet de stocker le code de l'API

## Pré-requis

- Python 3.14
- uv

## Instructions d'installation

```bash
git clone https://github.com/matthieu3344/projet-5---Deployez-un-modele-de-Machine-Learning
cd projet-5---Deployez-un-modele-de-Machine-Learning
uv sync
```

## Déploiement

à venir (étape 2)

## Authentification

à venir (étape 3)

## Tests

à venir (étape 5)

## Sécurisation

Les secrets (token Hugging Face & accès PostGreSQL) ne sont jamais commités (.env dans .gitignore, secrets GitHub)