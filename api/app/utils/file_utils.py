from fastapi import File, UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 50 * 1024 * 1024

async def process_file(file_path: Path) -> dict:
    try:
        file_size = file_path.stat().st_size

        chunk_size = 1024 * 1024
        content_preview = ""
        
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            content_preview = chunk.decode('utf-8', errors='ignore')[:1000]
        
        return {
            "file_size": file_size,
            "preview": content_preview,
            "status": "processed"
        }
    except Exception as e:
        logger.error(f"File processing failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

async def extract_file_content(file: UploadFile = File(...)):

    logger.info(f"Receiving upload: {file.filename} ({file.content_type})")
    
    allowed_types = ["application/pdf", "application/epub+zip", "text/plain"]
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"File too large: {file_size / (1024*1024):.2f} MB")
            file_path.unlink()
            raise HTTPException(status_code=400, detail="File too large")
        
        result = await process_file(file_path)
        file_path.unlink()
        
        return {
            "filename": file.filename,
            "processed_data": result
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))