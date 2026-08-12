from fastapi import APIRouter
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("")
def chat(request: ChatRequest) -> dict[str, str]:
    return {
        "session_id": request.session_id,
        "message": request.message,
    } 
