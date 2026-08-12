from enum import Enum

from pydantic import BaseModel

class ChunkingStrategy(str, Enum):
    RECURSIVE = "recursive",
    SENTENCE = "sentence"

class DocumentIngestionRequest(BaseModel):
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE