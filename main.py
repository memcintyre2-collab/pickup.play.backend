from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (Lovable) to access
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Sheet CSV link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ByNKk45KxiR-aC5kIiz4j0dhOvq-2fi-kxml6ZBCX0k/export?format=csv"

@app.get("/games")
def get_games():
    response = requests.get(SHEET_URL)
    return response.text  # raw CSV

@app.get("/recommend")
def recommend(sport: str):
    # Placeholder AI recommendation
    return {"recommendation": f"Try joining a {sport} pickup game near you!"}