import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/chatbot",
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_QUEUE_NAME = os.getenv("REDIS_QUEUE_NAME", "llm")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))

LLM_POOL_SIZE = int(os.getenv("LLM_POOL_SIZE", "3"))
LLM_MAX_CONCURRENT = int(os.getenv("LLM_MAX_CONCURRENT", "2"))
LLM_JOB_TIMEOUT = int(os.getenv("LLM_JOB_TIMEOUT", "120"))

DEFAULT_THREAD_ID = os.getenv("DEFAULT_THREAD_ID", "user-123")

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
