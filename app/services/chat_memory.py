import json

from app.schemas.chat import ChatMessage
from app.services.redis import RedisService

from typing import Any


class ChatMemoryService:
    def __init__(
        self,
        redis_service: RedisService,
    ) -> None:
        self.redis_service = redis_service

    def save_message(
        self,
        session_id: str,
        message: ChatMessage,
    ) -> None:
        key = f"chat:session:{session_id}"

        history = [
            existing_message.model_dump()
            for existing_message in self.get_history(session_id)
        ]

        history.append(message.model_dump())

        self.redis_service.client.set(
            key,
            json.dumps(history),
        )

    def get_history(
        self,
        session_id: str,
    ) -> list[ChatMessage]:
        key = f"chat:session:{session_id}"

        data = self.redis_service.client.get(key)

        if data is None:
            return []

        raw_history = json.loads(data)

        return [
            ChatMessage.model_validate(message)
            for message in raw_history
        ]

    def clear_history(
        self,
        session_id: str,
    ) -> None:
        key = f"chat:session:{session_id}"

        self.redis_service.client.delete(key)

    def get_booking_state(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        key = f"booking:session:{session_id}"

        data = self.redis_service.get(key)

        if data is None:
            return {}

        return json.loads(data)


    def save_booking_state(
        self,
        session_id: str,
        state: dict[str, Any],
    ) -> None:
        key = f"booking:session:{session_id}"

        self.redis_service.set(
            key,
            json.dumps(state),
        )

    def clear_booking_state(
        self,
        session_id: str,
    ) -> None:
        key = f"booking:session:{session_id}"

        self.redis_service.delete(key)

        