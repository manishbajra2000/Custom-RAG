from app.schemas.booking import BookingExtraction
from app.services.llm import LLMService


class BookingExtractor:
    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self.llm_service = llm_service

    def extract(
        self,
        message: str,
    ) -> BookingExtraction:
        prompt = f"""
You extract interview booking information from a user's message.

Extract these fields if they are explicitly present:
- name
- email
- date
- time

Do not invent or guess missing information.

Date must be returned in YYYY-MM-DD format.
Time must be returned in HH:MM 24-hour format.

Return ONLY valid JSON in exactly this format:

{{
    "name": null,
    "email": null,
    "date": null,
    "time": null
}}

User message:
{message}

JSON:
"""

        response = self.llm_service.generate(prompt)

        response = response.strip()
        
        if response.startswith("```json"):
            response = response[7:]
        
        if response.startswith("```"):
            response = response[3:]
        
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        return BookingExtraction.model_validate_json(response)