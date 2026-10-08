from chatbot.config import DEFAULT_THREAD_ID
from chatbot.service.chat import ChatService


def run_chat(thread_id: str = DEFAULT_THREAD_ID) -> None:
    chat_service = ChatService()
    config = chat_service.get_config(thread_id)

    print("Chatbot ready (Redis queue + streaming). Type 'bye' to exit.")
    print("Ensure worker is running: python -m worker.run\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        print("Bot: ", end="", flush=True)
        for token in chat_service.stream_tokens(user_input, thread_id):
            print(token, end="", flush=True)
        print("\n")

        if user_input.lower().startswith("bye"):
            print("Goodbye!")
            break
