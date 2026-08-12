from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from app.schemas.document import ChunkingStrategy
from app.services.document_extractor import extract_text

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = Form(...),
) -> dict[str, str]:
    try:
        text = await extract_text(file)
    except ValueError as exc:
        raise HTTPException(
            status_code=400, 
            detail=str(exc)
        ) from exc
    return {
        "filename": file.filename or "unknown",
        "chunking_strategy": chunking_strategy.value,
        "text_length": str(len(text)),
    }