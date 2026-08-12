from fastapi import APIRouter, Depends

from app.core.dependencies import get_chat_service
from app.schemas.chat import ChatRequest
from app.services.chat import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> dict[str, str]:

    answer = chat_service.chat(
        session_id=request.session_id,
        message=request.message,
    )

    return {
        "session_id": request.session_id,
        "answer": answer,
    }