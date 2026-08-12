import re

from app.schemas.document import ChunkingStrategy

DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100

def chunk_text(
        text: str,
        chunking_strategy: ChunkingStrategy,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> list[str]:
    if not text.strip():
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    if chunking_strategy == ChunkingStrategy.RECURSIVE:
        return recursive_chunk(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap 
        )

    if chunking_strategy == ChunkingStrategy.SENTENCE:
        return sentence_chunk(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    raise ValueError(f"Unsupported chunking strategy: {chunking_strategy}")

def recursive_chunk(
        text: str,
        chunk_size: int,
        chunk_overlap: int
) -> list[str]:
    separators = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]

    chunks = _recursive_split(text=text, separators=separators, chunk_size=chunk_size)

    return _add_overlap(chunks, chunk_overlap)

def _recursive_split(
    text: str,
    separators: list[str],
    chunk_size: int,
) -> list[str]:
    text = text.strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    if not separators:
        return [
            text[i : i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

    separator = separators[0]
    remaining_separators = separators[1:]

    if separator:
        parts = text.split(separator)
    else:
        parts = list(text)

    chunks: list[str] = []
    current = ""

    for part in parts:
        part = part.strip()

        if not part:
            continue

        candidate = (
            part
            if not current
            else f"{current}{separator}{part}"
        )

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current.strip())

        if len(part) <= chunk_size:
            current = part
        else:
            chunks.extend(
                _recursive_split(
                    part,
                    remaining_separators,
                    chunk_size,
                )
            )
            current = ""

    if current:
        chunks.append(current.strip())

    return chunks

def _add_overlap(
    chunks: list[str],
    overlap: int,
) -> list[str]:
    if overlap == 0 or len(chunks) <= 1:
        return chunks

    overlapped_chunks: list[str] = [chunks[0]]

    for index in range(1, len(chunks)):
        previous = chunks[index - 1]

        overlap_text = previous[-overlap:]

        current = f"{overlap_text} {chunks[index]}".strip()

        overlapped_chunks.append(current)

    return overlapped_chunks

def sentence_chunk(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    sentences = _split_sentences(text)

    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        candidate = (
            sentence
            if not current
            else f"{current} {sentence}"
        )

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())

            if len(sentence) > chunk_size:
                chunks.extend(
                    _recursive_split(
                        sentence,
                        [" ", ""],
                        chunk_size,
                    )
                )
                current = ""
            else:
                current = sentence

    if current:
        chunks.append(current.strip())

    return _add_overlap(chunks, chunk_overlap)

def _split_sentences(text: str) -> list[str]:
    sentences = text.replace("\n", " ")

    return [
        sentence.strip() for sentence in sentences.split(".") if sentence.strip()
    ]