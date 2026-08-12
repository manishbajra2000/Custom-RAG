from app.services.embeddings import EmbeddingService
from app.services.llm import LLMService
from app.services.qdrant import QdrantService


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        qdrant_service: QdrantService,
        llm_service: LLMService,
    ) -> None:
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service
        self.llm_service = llm_service

    def answer(
        self,
        question: str,
    ) -> str:
        query_vector = self.embedding_service.embed_text(question)

        results = self.qdrant_service.search(
            query_vector,
            limit=5,
        )

        context = "\n\n".join(
            result.payload["text"]
            for result in results
            if result.payload and "text" in result.payload
        )

        prompt = f"""
You are a helpful document assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

        return self.llm_service.generate(prompt)