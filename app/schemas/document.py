from enum import Enum

from pydantic import BaseModel

class ChunkingStrategy(str, Enum):
    RECURSIVE = "recursive",
    SENTENCE = "sentence"

class DocumentIngestionRequest(BaseModel):
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE

class IngestionResult(BaseModel):
    document_id: str
    filename: str
    chunk_count: int