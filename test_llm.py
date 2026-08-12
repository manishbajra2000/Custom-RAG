from app.services.llm import LLMService


llm = LLMService()

response = llm.generate(
    "Explain what a vector database is in one sentence."
)

print(response)