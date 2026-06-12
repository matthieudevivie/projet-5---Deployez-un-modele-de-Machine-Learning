from fastapi import FastAPI
from src.predictor import predire_attrition
from src.schemas import EmployeInput

app = FastAPI(title="API Attrition - Projet 5")


@app.get("/")
def racine():
    """Endpoint racine : prouve simplement que l'API est vivante."""
    return {"message": "L'API est en ligne", "statut": "ok"}


@app.get("/health")
def health():
    """Endpoint de santé : utilisé pour vérifier que le service répond."""
    return {"status": "healthy"}

@app.post("/predict")
def predict(employe: EmployeInput):
    return predire_attrition(employe)