from app.services.booking_extractor import BookingExtractor
from app.services.llm import LLMService


llm_service = LLMService()

extractor = BookingExtractor(
    llm_service=llm_service,
)


message = (
    "I'd like to book an interview. "
    "My name is Manish, my email is "
    "manish@example.com, on August 20 2026 at 3 PM."
)

result = extractor.extract(message)

print("Extracted booking information:")
print(result)