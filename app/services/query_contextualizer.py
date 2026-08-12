from app.schemas.chat import ChatMessage
from app.services.llm import LLMService


class QueryContextualizer:
    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self.llm_service = llm_service

    def contextualize(
        self,
        question: str,
        history: list[ChatMessage],
    ) -> str:

        if not history:
            return question

        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in history
        )

        prompt = f"""
You are a query contextualizer for a document question-answering system.

Rewrite the user's current question into a standalone question that
can be understood without the conversation history.

Use the conversation history to resolve references such as:
"it", "that", "they", "which one", "what does it", etc.

Do not answer the question.
Only return the rewritten standalone question.

Conversation history:
{conversation}

Current question:
{question}

Standalone question:
"""

        return self.llm_service.generate(prompt).strip()