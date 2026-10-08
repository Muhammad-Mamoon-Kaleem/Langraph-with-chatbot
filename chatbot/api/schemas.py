from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    thread_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    thread_id: str


class HealthResponse(BaseModel):
    status: str
    redis: str
    queue: str
