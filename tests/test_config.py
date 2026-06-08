from src.config import settings


def test_app_env_par_defaut():
    """Sans variable fournie (cas de la CI), l'environnement vaut 'dev'."""
    assert settings.app_env == "dev"