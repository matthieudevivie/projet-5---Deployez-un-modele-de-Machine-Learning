# Image de base : Python 3.14 avec uv déjà installé (fournie par Astral, créateurs de uv)
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie tout le projet dans la boîte
COPY . .

# Installe les bibliothèques système nécessaires à LightGBM
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Installe les dépendances Python, SANS les outils de dev
RUN uv sync --frozen --no-dev

# Rend le dossier importable (évite "ModuleNotFoundError: No module named 'src'")
ENV PYTHONPATH=/app

# Hugging Face s'attend à trouver l'application sur le port 7860
EXPOSE 7860

# Démarre le serveur : il sert l'objet "app" du fichier src/api.py
CMD ["/app/.venv/bin/uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "7860"]