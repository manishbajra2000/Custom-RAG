from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.dependencies import ingestion_service
from app.schemas.document import ChunkingStrategy


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    chunking_strategy: ChunkingStrategy = Form(...),
) -> dict[str, str]:
    try:
        document_id, chunk_count = (
            await ingestion_service.ingest_document(
                file,
                chunking_strategy,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "document_id": document_id,
        "filename": file.filename or "unknown",
        "chunking_strategy": chunking_strategy.value,
        "chunks_created": str(chunk_count),
    }