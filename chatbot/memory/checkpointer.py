from langgraph.checkpoint.postgres import PostgresSaver

from chatbot.config import DATABASE_URL


class Memory:
    def __init__(self):
        self.context = PostgresSaver.from_conn_string(DATABASE_URL)
        self.saver = self.context.__enter__()
        self.saver.setup()

    def get_saver(self):
        return self.saver

    def get_config(self, thread_id: str):
        return {
            "configurable": {
                "thread_id": thread_id,
            }
        }
