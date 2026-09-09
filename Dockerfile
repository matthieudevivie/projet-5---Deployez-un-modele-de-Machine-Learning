# Image de base : Python 3.14 avec uv déjà installé (fournie par Astral, créateurs de uv)
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Dépendance système de LightGBM (runtime OpenMP), absente de l'image "slim".
# Placée en premier : elle ne change jamais, sa couche est donc toujours réutilisée.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Les manifestes de dépendances SEULS. Tant qu'ils ne changent pas, Docker
# réutilise la couche d'installation ci-dessous, même si le code a changé.
COPY pyproject.toml uv.lock README.md ./

# Dépendances de production uniquement (--no-dev), versions figées (--frozen)
RUN uv sync --frozen --no-dev

# Le code applicatif en dernier : c'est ce qui change le plus souvent
COPY . .

# Rend le dossier importable (évite "ModuleNotFoundError: No module named 'src'")
ENV PYTHONPATH=/app

# Hugging Face s'attend à trouver l'application sur le port 7860
EXPOSE 7860

# Démarre le serveur : il sert l'objet "app" du fichier src/api.py
CMD ["/app/.venv/bin/uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "7860"]