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


# Un objet unique, importable partout : "from src.config import settings"
settings = Settings()