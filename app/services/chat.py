from app.schemas.chat import ChatMessage
from app.services.chat_memory import ChatMemoryService
from app.services.rag import RAGService


class ChatService:
    def __init__(
        self,
        memory_service: ChatMemoryService,
        rag_service: RAGService,
    ) -> None:
        self.memory_service = memory_service
        self.rag_service = rag_service

    def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:
        history = self.memory_service.get_history(
            session_id
        )

        user_message = ChatMessage(
            role="user",
            content=message,
        )

        answer = self.rag_service.answer(
            question=message,
            history=history,
        )

        self.memory_service.save_message(
            session_id,
            user_message,
        )

        self.memory_service.save_message(
            session_id,
            ChatMessage(
                role="assistant",
                content=answer,
            ),
        )

        return answer