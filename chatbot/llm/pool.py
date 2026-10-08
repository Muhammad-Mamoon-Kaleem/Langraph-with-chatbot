import threading

from langchain_ollama import ChatOllama

from chatbot.llm.client import create_llm


class LLMPool:
    """Round-robin pool of LLM client instances."""

    def __init__(self, size: int = 3):
        if size < 1:
            raise ValueError("pool size must be at least 1")

        self._llms: list[ChatOllama] = [create_llm() for _ in range(size)]
        self._index = 0
        self._lock = threading.Lock()

    @property
    def size(self) -> int:
        return len(self._llms)

    def get_llm(self) -> ChatOllama:
        with self._lock:
            llm = self._llms[self._index]
            self._index = (self._index + 1) % len(self._llms)
            return llm
