from app.schemas.booking import BookingExtraction
from app.services.booking_parser import BookingParser


parser = BookingParser()

extracted = BookingExtraction(
    name="Manish",
    email="manish@example.com",
    date="2026-08-20",
    time="15:00",
)

booking = parser.parse(extracted)

print("Parsed booking:")
print("Name:", booking.name)
print("Email:", booking.email)
print("Date:", booking.date)
print("Time:", booking.time)