"""
RQ task functions — executed by worker processes.

Run worker from project root:
    rq worker llm --url redis://localhost:6379
"""

from langchain_core.messages import messages_from_dict, messages_to_dict

from chatbot.config import LLM_POOL_SIZE
from chatbot.llm.pool import LLMPool

_pool = LLMPool(size=LLM_POOL_SIZE)


def process_llm(messages: list[dict]) -> dict:
    """
    Run LLM inference for a queued job.

    Args:
        messages: Serialized LangChain messages (list of dicts).

    Returns:
        Serialized assistant message dict (JSON-safe for Redis).
    """
    llm = _pool.get_llm()
    lc_messages = messages_from_dict(messages)
    response = llm.invoke(lc_messages)
    return messages_to_dict([response])[0]
