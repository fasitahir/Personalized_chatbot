from fastapi import FastAPI
from pydantic import BaseModel
from chat_history import store_message, get_recent_chat
from memory import save_to_memory, get_all_user_memory
from categorize import get_category
from config import GEMINI_API_KEY, MODEL_NAME
import google.generativeai as genai
import json
import re
import time

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

app = FastAPI()

class ChatInput(BaseModel):
    user_id: str
    message: str

@app.post("/chat/")
async def chat(input: ChatInput):
    start_time = time.perf_counter()  # Start timer
    user_id = input.user_id
    user_message = input.message
    
    # Store user message
    store_message(user_id, "user", user_message)

    # Retrieve all memory for context
    memory_facts = get_all_user_memory(user_id)
    memory_text = "\n".join(memory_facts)

    # Get recent chat history (last 5–10 messages)
    recent_history = get_recent_chat(user_id)
    history_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in recent_history])

    # Unified prompt for Gemini (response + fact extraction)
    full_prompt = f"""
You are a helpful, personalized assistant.

Here is the user's memory:
{memory_text}

Here is the recent conversation:
{history_text}

Current user message:
User: {user_message}

---

Instructions:
1. Generate a natural, helpful, and personalized reply.
2. Extract important personal/contextual facts (name, goals, likes, projects, preferences).
3. If no facts are found, leave facts list empty.

Respond in this JSON format:

{{
  "response": "<your personalized reply here>",
  "facts": [
    "fact 1",
    "fact 2"
  ]
}}
"""

    # Call Gemini
    response = model.generate_content(full_prompt)

    # Clean Gemini markdown-style response (if present)
    response_text = response.text
    cleaned_text = re.sub(r"^```json|```$", "", response_text.strip(), flags=re.MULTILINE).strip()

    # Parse response
    try:
        parsed = json.loads(cleaned_text)
    except json.JSONDecodeError:
        reply = response_text.strip()
        store_message(user_id, "assistant", reply)
        return {"response": reply, "warning": "Could not parse structured facts"}

    reply = parsed.get("response", "").strip()
    facts = parsed.get("facts", [])
    # Store the assistant's reply
    store_message(user_id, "assistant", reply)

    # Categorize and store extracted facts
    for fact in facts:
        category = get_category(fact)
        save_to_memory(user_id, category, fact)

    end_time = time.perf_counter()  # End timer
    latency = round(end_time - start_time, 2)  # in seconds
    print(f"Response latency: {latency} s")
    return {"response": reply}
