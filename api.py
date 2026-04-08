from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="System Wyceny Nieruchomości", description="API do przewidywania cen mieszkań")

# Dodajemy pozwolenie na komunikację z naszą stroną HTML (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W prawdziwym świecie wpisujemy tu adres naszej strony, "*" pozwala każdemu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ładujemy nasz wytrenowany model przy starcie serwera
model = joblib.load('moj_model_wyceny.pkl')

class Mieszkanie(BaseModel):
    Metraz: float
    Pokoje: int
    Wiek: int
    Dzielnica_Obrzeza: int
    Dzielnica_Przedmiescia: int

@app.get("/")
def powitanie():
    return FileResponse("index.html")

@app.post("/wycen")
def wycen_mieszkanie(dane: Mieszkanie):
    df = pd.DataFrame([dane.model_dump()]) # Używamy model_dump() (nowsza wersja pydantic)
    przewidywana_cena = model.predict(df)[0]
    return {
        "status": "sukces",
        "szacowana_cena_zl": round(przewidywana_cena, 2)
    }