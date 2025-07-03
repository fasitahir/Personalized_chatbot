from collections import defaultdict, deque

chat_store = defaultdict(lambda: deque(maxlen=10))

def store_message(user_id: str, role: str, content: str):
    chat_store[user_id].append({"role": role, "content": content})

def get_recent_chat(user_id: str):
    return list(chat_store[user_id])
