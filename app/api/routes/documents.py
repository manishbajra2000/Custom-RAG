from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from app.schemas.document import ChunkingStrategy
from app.services.ingestion import ingest_document

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
        chunks = await ingest_document(
        file,
        chunking_strategy,
    )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc
    return {
        "filename": file.filename or "unknown",
        "chunking_strategy": chunking_strategy.value,
        "text_length": str(len(chunks)),
    }