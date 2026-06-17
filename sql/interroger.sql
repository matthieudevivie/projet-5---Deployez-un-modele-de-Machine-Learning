-- ============================================================================
-- PROJET 5 - Etape 4 : Interrogation des donnees tracees
-- Requetes d'analyse sur les tables employes et predictions
-- ============================================================================


-- --- Requete 1 : historique des predictions d'un employe -------------------
-- Toutes les predictions faites pour un employe donne, de la plus recente
-- a la plus ancienne. Utile pour la tracabilite individuelle.
SELECT
    p.id                AS id_prediction,
    p.employe_id,
    p.attrition_predite,
    p.probabilite,
    p.seuil_utilise,
    p.date_prediction
FROM predictions AS p
WHERE p.employe_id = 2069          -- a remplacer par l'id recherche
ORDER BY p.date_prediction DESC;


-- --- Requete 2 : prediction vs realite (monitoring de performance) ---------
-- Croise la prediction du modele avec la verite terrain archivee.
-- Permet de mesurer si le modele "tape juste" en production.
-- Les employes dont la realite est encore inconnue (cible NULL, ex. nouvel
-- employe evalue via l'API) sont marques 'Inconnu' et non 'Erreur'.
SELECT
    e.id,
    e.poste,
    p.probabilite,
    p.attrition_predite                      AS predit_part,
    e.a_quitte_l_entreprise                  AS a_reellement_quitte,
    CASE
        WHEN e.a_quitte_l_entreprise IS NULL THEN 'Inconnu'
        WHEN (p.attrition_predite = TRUE  AND e.a_quitte_l_entreprise = 1)
          OR (p.attrition_predite = FALSE AND e.a_quitte_l_entreprise = 0)
        THEN 'Correct'
        ELSE 'Erreur'
    END                                       AS verdict
FROM predictions AS p
INNER JOIN employes AS e ON e.id = p.employe_id;


-- --- Requete 3 : taux de bonnes predictions (vue agregee) ------------------
-- Resume chiffre de la performance : combien de predictions correctes.
-- On ne compte que les employes dont la realite est connue (cible NON NULL).
SELECT
    COUNT(*)                                                   AS total_predictions,
    SUM(CASE
            WHEN (p.attrition_predite = TRUE  AND e.a_quitte_l_entreprise = 1)
              OR (p.attrition_predite = FALSE AND e.a_quitte_l_entreprise = 0)
            THEN 1 ELSE 0
        END)                                                   AS predictions_correctes,
    ROUND(
        100.0 * SUM(CASE
            WHEN (p.attrition_predite = TRUE  AND e.a_quitte_l_entreprise = 1)
              OR (p.attrition_predite = FALSE AND e.a_quitte_l_entreprise = 0)
            THEN 1 ELSE 0
        END) / COUNT(*), 1)                                    AS taux_precision_pct
FROM predictions AS p
INNER JOIN employes AS e ON e.id = p.employe_id
WHERE e.a_quitte_l_entreprise IS NOT NULL;


-- --- Requete 4 : employes a risque detectes recemment ----------------------
-- Vue RH actionnable : les profils predits "a risque", tries par probabilite.
SELECT
    e.id,
    e.poste,
    e.revenu_mensuel,
    p.probabilite,
    p.date_prediction
FROM predictions AS p
INNER JOIN employes AS e ON e.id = p.employe_id
WHERE p.attrition_predite = TRUE
ORDER BY p.probabilite DESC
LIMIT 20;