from app.models.Character import Character
from app.services.neo4j.CharacterGraph import CharacterGraph
from api.app.services.pinecone import BaseAdapter
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline.core import pipeline_core
from app.models.UserInput import UserInput
from dotenv import load_dotenv
import os
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Application is starting...")
    load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = openai_key
    print("Startup tasks completed.")

@app.post("/init_pinecone")
async def init_pc():
    
    # WIP add some basic data to Pinecone
    adapter = BaseAdapter()
    adapter.create_index()
    data = [
        {'id': 'fact1', 'text': 'Testopia is a mythical land where all trials of skill, logic, and endurance are sent to be tested for their worth.'},
        {'id': 'fact2', 'text': 'The Testmasters Guild, founded centuries ago, holds an annual event called the Trial of Triumph to determine the sharpest mind in the realm.'},
        {'id': 'fact3', 'text': 'John, a swift and ambitious adventurer, has a long-standing aversion to testing, believing it slows him down and wastes precious time.'},
        {'id': 'fact4', 'text': 'Legends speak of the Puzzle of Infinity, a test so complex that even the founders of Testopia, Testar, Solvet, and Examina, could not solve it.'},
        {'id': 'fact5', 'text': 'In Testopia, the saying "A test unattempted is a lesson unlearned" is inscribed on the gates of the Guild’s great hall.'},
        {'id': 'fact6', 'text': 'John’s aversion to testing stems from a failed attempt at the Maze of Mirrors, where he lost precious weeks trying to navigate its reflective puzzles.'},
        {'id': 'fact7', 'text': 'The Testmasters Guild has recently begun experimenting with interactive, real-time tests designed to challenge even the fastest thinkers like John.'},
        {'id': 'fact8', 'text': 'Many citizens of Testopia view testing as a sacred ritual, while others, like John, see it as a frustrating obstacle to progress.'}
    ]

    adapter.upsert_data(data)
    return

@app.post("/send_input")
async def ai_request(input_data: UserInput):
    return StreamingResponse(pipeline_core(input_data.user_input), media_type="application/json")