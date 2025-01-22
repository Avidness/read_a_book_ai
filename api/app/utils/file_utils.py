from fastapi import File, UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid
import logging
import PyPDF2
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 50 * 1024 * 1024

async def process_file(file_path: Path) -> dict:
    try:
        file_size = file_path.stat().st_size
        content = ""
        
        if file_path.suffix.lower() == '.pdf':
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                content = '\n'.join(page.extract_text() for page in pdf_reader.pages)
        
        elif file_path.suffix.lower() == '.epub':
            logger.info(f"epub")
            book = epub.read_epub(str(file_path))
            logger.info(f"epub2")
            texts = []
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                soup = BeautifulSoup(item.content, 'html.parser')
                texts.append(soup.get_text())
            content = '\n'.join(texts)
        
        else:  # text file
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
        
        return {
            "file_size": file_size,
            "text_content": content,
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
    

def chunkify_textblob(text, chunk_size=10000, overlap=100):
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Find word boundary within overlap region
        if end < len(text):
            search_end = min(end + overlap, len(text))
            next_space = text.rfind(' ', end, search_end)
            if next_space != -1:
                end = next_space
        else:
            end = len(text)
        
        chunks.append(text[start:end].strip())
        
        if end == len(text):
            break
        
        # Adjust start position for next chunk
        start = end - overlap
        next_word = text.find(' ', start)
        if next_word != -1 and next_word - start < overlap:
            start = next_word + 1

    return chunks