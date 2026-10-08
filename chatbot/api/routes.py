from fastapi import APIRouter, HTTPException

from chatbot.api.schemas import ChatRequest, ChatResponse, HealthResponse
from chatbot.config import DEFAULT_THREAD_ID, REDIS_QUEUE_NAME
from chatbot.queue.connection import get_redis, get_queue
from chatbot.service.chat import ChatService

router = APIRouter()
chat_service = ChatService()


@router.get("/health", response_model=HealthResponse)
def health():
    try:
        get_redis().ping()
        redis_status = "ok"
    except Exception:
        redis_status = "error"

    queue = get_queue()
    return HealthResponse(
        status="ok" if redis_status == "ok" else "degraded",
        redis=redis_status,
        queue=f"{REDIS_QUEUE_NAME} ({len(queue)} waiting)",
    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    thread_id = request.thread_id or DEFAULT_THREAD_ID

    try:
        reply = chat_service.chat(request.message, thread_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(reply=reply, thread_id=thread_id)
