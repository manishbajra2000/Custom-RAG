from datetime import date, time

from app.schemas.booking import BookingCreate, BookingExtraction


class BookingParser:
    def parse(
        self,
        extracted: BookingExtraction,
    ) -> BookingCreate:
        if not extracted.name:
            raise ValueError("Name is required.")

        if not extracted.email:
            raise ValueError("Email is required.")

        if not extracted.date:
            raise ValueError("Interview date is required.")

        if not extracted.time:
            raise ValueError("Interview time is required.")

        return BookingCreate(
            name=extracted.name,
            email=extracted.email,
            date=date.fromisoformat(extracted.date),
            time=time.fromisoformat(extracted.time),
        )