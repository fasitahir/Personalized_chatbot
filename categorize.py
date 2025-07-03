from functools import lru_cache
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

@lru_cache(maxsize=500)
def get_category(user_query: str) -> str:
    query = user_query.lower()

    profile_keywords = ["i am", "my name is", "people call me", "i'm", "i am called"]
    preference_keywords = ["like", "prefer", "love", "enjoy", "hate", "interested in"]
    project_keywords = ["project", "working on", "building", "developing", "researching", "creating"]

    for kw in profile_keywords:
        if kw in query:
            return "profile"
    
    for kw in preference_keywords:
        if kw in query:
            return "preferences"
    
    for kw in project_keywords:
        if kw in query:
            return "projects"
    
    if len(query.split()) < 3:
        return "general"

    # Fallback to Gemini
    prompt = f"""
Classify the following user message into one of the categories below:

- profile → if the user talks about name, identity, age, or background
- preferences → if the user mentions likes, dislikes, interests, or hobbies
- projects → if the user talks about work, studies, or building/creating something
- general → if none apply

Just return one of: profile, preferences, projects, or general.

Message: "{user_query}"
"""
    response = model.generate_content(prompt)
    category = response.text.strip().lower()
    category = category.strip('".*` ')

    valid = {"profile", "preferences", "projects", "general"}
    return category if category in valid else "general"
