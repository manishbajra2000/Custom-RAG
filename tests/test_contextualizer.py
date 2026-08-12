from app.schemas.chat import ChatMessage
from app.services.llm import LLMService
from app.services.query_contextualizer import QueryContextualizer


llm_service = LLMService()

contextualizer = QueryContextualizer(
    llm_service=llm_service,
)

history = [
    ChatMessage(
        role="user",
        content="What are the four houses at Hogwarts?",
    ),
    ChatMessage(
        role="assistant",
        content=(
            "The four houses are Gryffindor, Hufflepuff, "
            "Ravenclaw, and Slytherin."
        ),
    ),
]

question = "Which one is Harry in?"

standalone_question = contextualizer.contextualize(
    question=question,
    history=history,
)

print("Original:")
print(question)

print("\nStandalone:")
print(standalone_question)