from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
from fastapi.responses import JSONResponse
import os
from groq import Groq

app = FastAPI()

# Allow frontend (Lovable) to access
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Groq AI
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Google Sheet CSV link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ByNKk45KxiR-aC5kIiz4j0dhOvq-2fi-kxml6ZBCX0k/export?format=csv"

# Return games as JSON
@app.get("/games")
def get_games():
    response = requests.get(SHEET_URL)
    f = io.StringIO(response.text)
    reader = csv.DictReader(f)
    games = list(reader)
    return JSONResponse(content=games)

# AI Recommendation endpoint
@app.get("/recommend")
def recommend(sport: str):

    prompt = f"""
    Suggest a fun pickup {sport} game someone could join in San Francisco.
    Mention a park or public court if possible. Keep it short and friendly.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192"
    )

    recommendation = chat_completion.choices[0].message.content

    return {"recommendation": recommendation}
