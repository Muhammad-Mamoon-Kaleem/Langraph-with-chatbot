from chatbot.config import DEFAULT_THREAD_ID
from chatbot.graph.builder import build_graph
from chatbot.memory.checkpointer import Memory
from chatbot.utils import get_content


class ChatService:
    def __init__(self):
        self.memory = Memory()
        self.graph = build_graph(self.memory)

    def get_config(self, thread_id: str) -> dict:
        return self.memory.get_config(thread_id)

    def chat(self, message: str, thread_id: str = DEFAULT_THREAD_ID) -> str:
        config = self.get_config(thread_id)
        result = self.graph.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config,
        )
        return get_content(result["messages"][-1])

    def stream_tokens(self, message: str, thread_id: str = DEFAULT_THREAD_ID):
        config = self.get_config(thread_id)
        for message_chunk, _metadata in self.graph.stream(
            {"messages": [{"role": "user", "content": message}]},
            config,
            stream_mode="messages",
        ):
            token = get_content(message_chunk)
            if token:
                yield token
