from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.processor import InputProcessor
from app.services.generator import ContentEngine
from app.services.tutor import AITutor
from app.services.exporter import ExportEngine
import shutil

router = APIRouter()

# Initialize services
processor = InputProcessor()
content_engine = ContentEngine()
tutor = AITutor()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    file_location = f"temp_{file.filename}"
    
    # Save temp file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process Input
    raw_text = processor.auto_process(file_location, file.content_type.split('/')[-1])
    
    # Trigger Async Processing (Notes Generation + Embedding)
    # In a real app, this goes to Celery
    # background_tasks.add_task(content_engine.generate_indepth_notes, raw_text)
    
    # Synchronous example for demo
    notes = content_engine.generate_indepth_notes(raw_text)
    
    return {"status": "processed", "notes_preview": notes[:500]}

@router.post("/doubt")
async def solve_doubt(query: str):
    answer = tutor.solve_doubt(query)
    return {"answer": answer}

@router.get("/cheatsheet/export")
async def export_cheatsheet(content: str):
    filepath = ExportEngine.generate_cheatsheet_pdf(content, "prepify_cheatsheet.pdf")
    return {"download_url": filepath}
