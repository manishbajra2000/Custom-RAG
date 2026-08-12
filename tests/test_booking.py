from datetime import date, time

from app.db.database import SessionLocal
from app.schemas.booking import BookingCreate
from app.services.booking import BookingService


db = SessionLocal()

booking_service = BookingService()

booking_data = BookingCreate(
    name="Manish",
    email="manish@example.com",
    date=date(2026, 8, 20),
    time=time(15, 0),
)

booking = booking_service.create_booking(
    db=db,
    booking_data=booking_data,
)

print("Booking created:")
print("ID:", booking.id)
print("Name:", booking.name)
print("Email:", booking.email)
print("Date:", booking.interview_date)
print("Time:", booking.interview_time)

db.close()