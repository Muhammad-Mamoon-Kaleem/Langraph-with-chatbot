import sys
import time

from langchain_core.messages import BaseMessage, messages_from_dict, messages_to_dict
from rq.job import JobStatus

from chatbot.config import LLM_JOB_TIMEOUT
from chatbot.queue.connection import get_queue
from chatbot.queue.tasks import process_llm


def _serialize_messages(messages: list) -> list[dict]:
    if not messages:
        return []
    if isinstance(messages[0], dict):
        return messages
    return messages_to_dict(messages)


def _wait_for_result(job, timeout: int):
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        job.refresh()
        status = job.get_status(refresh=False)

        if status == JobStatus.FINISHED:
            value = job.return_value(refresh=True)
            if value is not None:
                return value

        if status == JobStatus.FAILED:
            raise RuntimeError(job.exc_info or "LLM job failed")

        if status == JobStatus.STOPPED:
            raise RuntimeError("LLM job was stopped")

        time.sleep(0.25)

    raise TimeoutError(f"LLM job timed out after {timeout}s")


def submit_llm(messages: list[BaseMessage], timeout: int | None = None) -> BaseMessage:
    """
    Enqueue an LLM job, wait for a worker, and return the assistant message.
    """
    queue = get_queue()
    serialized = _serialize_messages(messages)
    job = queue.enqueue(process_llm, serialized)
    wait_timeout = timeout or LLM_JOB_TIMEOUT

    try:
        result_dict = _wait_for_result(job, wait_timeout)
    except TimeoutError as exc:
        hint = "Start the worker:\n  python -m worker.run"
        if sys.platform == "win32":
            hint += "  (uses SimpleWorker on Windows)"
        raise RuntimeError(
            f"LLM job timed out. Is Redis running and is the worker started?\n{hint}"
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            "LLM job failed. Is Redis running and is the worker started?\n"
            "  docker start redis\n"
            "  python -m worker.run"
        ) from exc

    return messages_from_dict([result_dict])[0]
