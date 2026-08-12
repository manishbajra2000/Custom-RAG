from datetime import date, time

from pydantic import BaseModel, EmailStr


class BookingCreate(BaseModel):
    name: str
    email: EmailStr
    date: date
    time: time


class BookingExtraction(BaseModel):
    name: str | None = None
    email: str | None = None
    date: str | None = None
    time: str | None = None