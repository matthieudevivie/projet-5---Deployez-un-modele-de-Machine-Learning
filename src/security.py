"""Authentification de l'API par clé partagée (API key).

Le client doit fournir un en-tête HTTP `X-API-Key`. Sa valeur est comparée
à celle de la configuration. Aucune notion d'utilisateur ici : c'est une
clé de service, adaptée à un POC consommé par un outil RH interne.
"""

import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.config import settings

NOM_ENTETE = "X-API-Key"

# APIKeyHeader déclare le schéma de sécurité DANS OpenAPI : c'est cet objet
# qui fait apparaître le bouton "Authorize" et les cadenas dans Swagger.
# auto_error=False : on gère nous-mêmes le message d'erreur ci-dessous.
entete_api_key = APIKeyHeader(
    name=NOM_ENTETE,
    auto_error=False,
    description="Clé d'API fournie par l'équipe. À coller dans le bouton Authorize.",
)


def verifier_cle_api(cle_recue: str | None = Security(entete_api_key)) -> str:
    """Dépendance FastAPI : laisse passer si la clé est valide, sinon lève 401."""
    if not settings.api_key:
        # Mauvaise configuration du serveur, pas une faute du client.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Aucune clé d'API n'est configurée côté serveur.",
        )

    # compare_digest : comparaison à temps constant, pour ne pas laisser
    # fuiter la clé caractère par caractère via le temps de réponse.
    if cle_recue is None or not secrets.compare_digest(cle_recue, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé d'API absente ou invalide.",
        )

    return cle_recue