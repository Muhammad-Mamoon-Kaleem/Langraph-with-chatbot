def get_content(message) -> str:
    if isinstance(message, dict):
        return message["content"]
    content = message.content
    if isinstance(content, str):
        return content
    return str(content)
