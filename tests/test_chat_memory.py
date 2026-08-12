from app.schemas.chat import ChatMessage
from app.services.chat_memory import ChatMemoryService
from app.services.redis import RedisService


redis_service = RedisService()
memory = ChatMemoryService(redis_service)

session_id = "test-session"

memory.clear_history(session_id)

memory.save_message(
    session_id,
    ChatMessage(
        role="user",
        content="My name is Manish.",
    ),
)

memory.save_message(
    session_id,
    ChatMessage(
        role="assistant",
        content="Nice to meet you, Manish.",
    ),
)

memory.save_message(
    session_id,
    ChatMessage(
        role="user",
        content="What is my name?",
    ),
)

history = memory.get_history(session_id)

for message in history:
    print(message.role, ":", message.content)