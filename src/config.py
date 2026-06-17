from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Dit à pydantic : "si un fichier .env existe, lis-le" (pratique en local).
    # extra="ignore" => on ne plante pas si .env contient des variables en trop.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Quel environnement ? "dev" par défaut.
    # En prod, on fournira la variable APP_ENV=prod (sans toucher au code).
    app_env: str = "dev"

    # Un secret. Sa valeur par défaut est VIDE : jamais de vrai token dans le code.
    # Il sera fourni par .env en local, et par un secret GitHub/HF en prod.
    hf_token: str = ""

    # --- Base de données --------------------------------------------------
    # Interrupteur : la base n'est activée que si DB_ENABLED=true dans le .env.
    # En local on l'active ; sur Hugging Face on ne le met pas (donc False).
    db_enabled: bool = False

    # Paramètres de connexion. Valeurs par défaut adaptées au local (pas de
    # mot de passe). En prod, fournis via secrets sans toucher au code.
    db_user: str = "postgres"
    db_password: str = ""
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "futurisys"


# Un objet unique, importable partout : "from src.config import settings"
settings = Settings()