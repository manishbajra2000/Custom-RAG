from app.schemas.document import ChunkingStrategy
from app.services.chunking import chunk_text

with open("harrypotter.txt", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(
    text,
    ChunkingStrategy.SENTENCE,
)

print(len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- CHUNK {i} ---")
    print(chunk)