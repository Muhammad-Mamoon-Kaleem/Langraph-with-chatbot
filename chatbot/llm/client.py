from langchain_ollama import ChatOllama

from chatbot.config import OLLAMA_MODEL, OLLAMA_TEMPERATURE


def create_llm() -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=OLLAMA_TEMPERATURE,
    )


def get_llm() -> ChatOllama:
    llm = create_llm()
    print(f"LLM initialized successfully (Ollama {OLLAMA_MODEL}).")
    return llm
