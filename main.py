from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
from fastapi.responses import JSONResponse

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

# ✅ Return JSON instead of CSV
@app.get("/games")
def get_games():
    response = requests.get(SHEET_URL)
    f = io.StringIO(response.text)
    reader = csv.DictReader(f)
    games = list(reader)
    return JSONResponse(content=games)

# Recommendation endpoint
@app.get("/recommend")
def recommend(sport: str):
    return {"recommendation": f"Try joining a {sport} pickup game near you!"}
