from langgraph.graph import END, START, StateGraph

from chatbot.graph.nodes import chatbot
from chatbot.memory.checkpointer import Memory
from chatbot.state import State


def build_graph(memory: Memory):
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    return builder.compile(checkpointer=memory.get_saver())
