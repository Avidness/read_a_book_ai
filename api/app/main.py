from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline.write_a_book import generate_book
from app.pipeline.read_a_book import process_book
from app.models.UserInput import UserInput
from dotenv import load_dotenv
import os
from pathlib import Path
import shutil
import uuid
import logging

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
MAX_FILE_SIZE = 50 * 1024 * 1024

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
async def process_book(input_data: UserInput):
    return StreamingResponse(process_book(input_data.user_input), media_type="application/json")

@app.post("/upload2")
async def upload_file(file: UploadFile = File(...)):
    return StreamingResponse(process_book(file), media_type="application/json")

@app.post("/write_a_book")
async def generate_book(input_data: UserInput):
    return StreamingResponse(generate_book(input_data.user_input), media_type="application/json")

async def process_file(file_path: Path) -> dict:
    try:
        logger.debug(f"Processing file: {file_path}")
        file_size = file_path.stat().st_size
        logger.debug(f"File size: {file_size / (1024*1024):.2f} MB")

        chunk_size = 1024 * 1024
        content_preview = ""
        
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            content_preview = chunk.decode('utf-8', errors='ignore')[:1000]
        
        logger.debug(f"Preview length: {len(content_preview)} chars")
        return {
            "file_size": file_size,
            "preview": content_preview,
            "status": "processed"
        }
    except Exception as e:
        logger.error(f"File processing failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")



@app.post("/upload2")
async def upload_file(file: UploadFile = File(...)):
    return StreamingResponse(process_book(file), media_type="application/json")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    logger.info(f"Receiving upload: {file.filename} ({file.content_type})")
    
    allowed_types = ["application/pdf", "application/epub+zip", "text/plain"]
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    logger.debug(f"Generated unique path: {file_path}")
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.debug(f"File saved to disk: {file_path}")
        
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"File too large: {file_size / (1024*1024):.2f} MB")
            file_path.unlink()
            raise HTTPException(status_code=400, detail="File too large")
        
        result = await process_file(file_path)
        file_path.unlink()
        
        logger.info(f"Upload processed successfully: {file.filename}")
        return {
            "filename": file.filename,
            "processed_data": result
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))