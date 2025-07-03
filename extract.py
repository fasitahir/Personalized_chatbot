import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def extract_facts(user_query: str) -> list[str]:
    prompt = f"""
Extract useful facts from the following user statement.

Only include **personal or contextual facts** like:
- Name
- Location
- Job or study
- Preferences (likes/dislikes)
- Goals or future plans
- Hobbies or interests
- Important current activity (e.g., working on a project)

Return a plain list with each fact on a new line.

👉 If there are **no useful or important facts**, return **nothing**.

User statement: "{user_query}"
"""
    response = model.generate_content(prompt)
    facts = response.text.strip().split("\n")
    
    return [
        fact.strip("-• ").strip()
        for fact in facts
        if fact.strip() and not fact.lower().startswith("no")  # Filter "No facts found" etc.
    ]
