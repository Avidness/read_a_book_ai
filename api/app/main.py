from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from api.app.pipeline.write_a_book import generate_book
from api.app.pipeline.read_a_book import process_book
from app.models.UserInput import UserInput
from dotenv import load_dotenv
import os

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

@app.post("/read_a_book")
async def ai_request(input_data: UserInput):
    return StreamingResponse(process_book(input_data.user_input), media_type="application/json")

@app.post("/write_a_book")
async def ai_request(input_data: UserInput):
    return StreamingResponse(generate_book(input_data.user_input), media_type="application/json")