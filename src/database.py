"""Connexion à la base PostgreSQL et définition des tables (ORM SQLAlchemy)."""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings

# --- Connexion ------------------------------------------------------------

# Toute la configuration vient de settings, qui lit le .env automatiquement
# (via pydantic-settings). Plus besoin de 'source .env' dans le terminal.
DB_ENABLED = settings.db_enabled

# Si un mot de passe existe, on l'insère ; sinon on le laisse vide (local trust).
_auth = (
    f"{settings.db_user}:{settings.db_password}"
    if settings.db_password
    else settings.db_user
)
DATABASE_URL = (
    f"postgresql+psycopg2://{_auth}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(DATABASE_URL)

# La "fabrique de sessions" : chaque session est une conversation avec la base.
SessionLocal = sessionmaker(bind=engine)


def get_session():
    """Dépendance FastAPI : fournit une session et la referme automatiquement.

    Le 'yield' donne la session à l'endpoint ; le bloc 'finally' s'exécute
    une fois la réponse envoyée, garantissant que la session est toujours fermée.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Le "moule" dont héritent toutes les tables.
Base = declarative_base()


# --- Table 1 : les employés (les inputs du modèle) ------------------------

class Employe(Base):
    __tablename__ = "employes"

    # Clé primaire : accepte un id fourni (dataset historique, ids du SIRH)
    # ET en génère un automatiquement si aucun n'est donné (nouvel employé via API).
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Vérité terrain archivée pour le monitoring (départ réel : 0 = reste, 1 = parti).
    # Stockée mais JAMAIS envoyée au modèle pour prédire.
    a_quitte_l_entreprise = Column(Integer)

    # Notes de satisfaction et d'évaluation (1 à 4)
    satisfaction_employee_environnement = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_precedente = Column(Integer)
    note_evaluation_actuelle = Column(Integer)

    # Caractéristiques personnelles et professionnelles
    heure_supplementaires = Column(String)
    age = Column(Integer)
    genre = Column(String)
    revenu_mensuel = Column(Integer)
    statut_marital = Column(String)
    poste = Column(String)

    # Expérience et formation
    nombre_experiences_precedentes = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    distance_domicile_travail = Column(Integer)

    # Éducation et carrière
    niveau_education = Column(Integer)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    annees_depuis_la_derniere_promotion = Column(Integer)


# --- Table 2 : les prédictions (les outputs du modèle) --------------------

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    employe_id = Column(Integer, ForeignKey("employes.id"))
    attrition_predite = Column(Boolean)
    probabilite = Column(Float)
    seuil_utilise = Column(Float)
    date_prediction = Column(DateTime, default=lambda: datetime.now(timezone.utc))