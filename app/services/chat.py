from sqlalchemy.orm import Session

from app.schemas.booking import BookingExtraction
from app.schemas.chat import ChatMessage
from app.services.booking import BookingService
from app.services.booking_extractor import BookingExtractor
from app.services.booking_parser import BookingParser
from app.services.chat_memory import ChatMemoryService
from app.services.rag import RAGService


class ChatService:
    def __init__(
        self,
        memory_service: ChatMemoryService,
        rag_service: RAGService,
        booking_service: BookingService,
        booking_extractor: BookingExtractor,
        booking_parser: BookingParser,
    ) -> None:
        self.memory_service = memory_service
        self.rag_service = rag_service
        self.booking_service = booking_service
        self.booking_extractor = booking_extractor
        self.booking_parser = booking_parser

    def _is_booking_request(
        self,
        message: str,
    ) -> bool:
        booking_keywords = (
            "book an interview",
            "book interview",
            "schedule an interview",
            "schedule interview",
            "interview booking",
        )

        message_lower = message.lower()

        return any(
            keyword in message_lower
            for keyword in booking_keywords
        )

    def chat(
        self,
        session_id: str,
        message: str,
        db: Session,
    ) -> str:
        history = self.memory_service.get_history(
            session_id
        )

        user_message = ChatMessage(
            role="user",
            content=message,
        )

        booking_state = self.memory_service.get_booking_state(
            session_id
        )

        # Continue an existing booking
        if booking_state:
            extracted = self.booking_extractor.extract(
                message
            )

            booking_state.update(
                extracted.model_dump(
                    exclude_none=True
                )
            )

            self.memory_service.save_booking_state(
                session_id,
                booking_state,
            )

            missing_fields = [
                field
                for field in (
                    "name",
                    "email",
                    "date",
                    "time",
                )
                if not booking_state.get(field)
            ]

            if missing_fields:
                answer = (
                    "I still need your "
                    + ", ".join(missing_fields)
                    + "."
                )

            else:
                try:
                    booking_extraction = BookingExtraction(
                        name=booking_state["name"],
                        email=booking_state["email"],
                        date=booking_state["date"],
                        time=booking_state["time"],
                    )

                    booking_data = self.booking_parser.parse(
                        extracted=booking_extraction
                    )

                    booking = self.booking_service.create_booking(
                        db=db,
                        booking_data=booking_data,
                    )

                    self.memory_service.clear_booking_state(
                        session_id
                    )

                    answer = (
                        "Your interview has been booked successfully "
                        f"for {booking.interview_date} at "
                        f"{booking.interview_time}."
                    )

                except ValueError as exc:
                    answer = str(exc)

        # Start a new booking
        elif self._is_booking_request(message):
            extracted = self.booking_extractor.extract(
                message
            )

            booking_state = extracted.model_dump(
                exclude_none=True
            )

            self.memory_service.save_booking_state(
                session_id,
                booking_state,
            )

            missing_fields = [
                field
                for field in (
                    "name",
                    "email",
                    "date",
                    "time",
                )
                if not booking_state.get(field)
            ]

            if missing_fields:
                answer = (
                    "Sure. I need your "
                    + ", ".join(missing_fields)
                    + " to book the interview."
                )

            else:
                try:
                    booking_data = self.booking_parser.parse(
                        extracted=extracted
                    )

                    booking = self.booking_service.create_booking(
                        db=db,
                        booking_data=booking_data,
                    )

                    self.memory_service.clear_booking_state(
                        session_id
                    )

                    answer = (
                        "Your interview has been booked successfully "
                        f"for {booking.interview_date} at "
                        f"{booking.interview_time}."
                    )

                except ValueError as exc:
                    answer = str(exc)

        # Normal RAG
        else:
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