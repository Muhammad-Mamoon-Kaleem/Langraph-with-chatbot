from chatbot.queue.client import submit_llm
from chatbot.state import State


def chatbot(state: State):
    response = submit_llm(state["messages"])
    return {"messages": [response]}
