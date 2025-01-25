from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline.write_a_book import generate_book
from app.pipeline.read_a_book import process_book
from app.models.user_input import UserInput
from dotenv import load_dotenv
import os
from pathlib import Path
import logging
from app.utils.file_utils import extract_file_content

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting...")
    
    load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = openai_key
    
    for file in UPLOAD_DIR.glob("*"):
        file.unlink()
    
    logger.info("Startup tasks completed")

@app.post("/read_a_book")
async def read_a_book(file: UploadFile = File(...)):
    result = await extract_file_content(file)
    return StreamingResponse(process_book(result), media_type="text/event-stream")

@app.post("/write_a_book")
async def write_a_book(input_data: UserInput):
    return StreamingResponse(generate_book(input_data.user_input), media_type="application/json")
