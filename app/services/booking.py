from sqlalchemy.orm import Session

from app.db.models import Booking
from app.schemas.booking import BookingCreate


class BookingService:
    def create_booking(
        self,
        db: Session,
        booking_data: BookingCreate,
    ) -> Booking:
        booking = Booking(
            name=booking_data.name,
            email=booking_data.email,
            interview_date=booking_data.date,
            interview_time=booking_data.time,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking