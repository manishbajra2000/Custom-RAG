from app.schemas.document import ChunkingStrategy
from app.services.chunking import chunk_text


def test_recursive_chunking() -> None:
    text = (
        "This is sentence one. "
        "This is sentence two. "
        "This is sentence three."
    )

    chunks = chunk_text(
        text,
        ChunkingStrategy.RECURSIVE,
        chunk_size=40,
        chunk_overlap=5,
    )

    assert chunks
    assert all(chunks)

def test_sentence_chunking() -> None:
    text = (
        "This is sentence one. "
        "This is sentence two. "
        "This is sentence three."
    )

    chunks = chunk_text(
        text,
        ChunkingStrategy.SENTENCE,
        chunk_size=40,
        chunk_overlap=5,
    )

    assert chunks
    assert all(chunks)