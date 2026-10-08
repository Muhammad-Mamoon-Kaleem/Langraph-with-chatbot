from fastapi import FastAPI

from chatbot.api.routes import router

app = FastAPI(
    title="LangGraph Memory Chatbot",
    description="Chatbot with Postgres memory and Redis LLM queue",
    version="1.0.0",
)

app.include_router(router)
