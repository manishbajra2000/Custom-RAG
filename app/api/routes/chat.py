from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_chat_service
from app.db.database import get_db
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
    db: Session = Depends(get_db),
) -> dict[str, str]:

    answer = chat_service.chat(
        session_id=request.session_id,
        message=request.message,
        db=db,
    )

    return {
        "session_id": request.session_id,
        "answer": answer,
    }