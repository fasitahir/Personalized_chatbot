# 🤖 Memory-Enhanced Personalized Chatbot

A smart chatbot that remembers **who you are**! This project leverages the **Google Gemini API**, **FastAPI**, **Redis**, and **Streamlit** to create a personalized chat experience with both:

- 🧠 **Short-term memory** (recent chat history)
- 💾 **Long-term memory** (persistent user facts)

---

## 📌 Features

- 🧠 **Memory-aware assistant** — stores and recalls user details like name, location, preferences, and projects.
- 🔁 **Short-term memory** — remembers recent conversation context (last 5–10 messages).
- 💾 **Long-term memory** — uses Redis to persist meaningful user facts.
- ⚡ **FastAPI backend** — serves structured LLM responses powered by Gemini.
- 🎯 **Streamlit frontend** — clean, responsive user interface.
- 🛠️ **Fact extraction** — extracts structured personal facts for storage.

---

## 🧠 How It Works

### 🔹 Short-Term Memory
Short-term memory stores the last few messages exchanged with the user to maintain contextual continuity. These are injected into prompts sent to the model.

### 🔹 Long-Term Memory (Redis)
Facts are extracted by Gemini and stored in Redis, organized into categories:
user:<user_id>:memory:<category>


Categories include:

- `profile`: Name, location, age, etc.
- `projects`: Work or academic projects
- `preferences`: Likes, dislikes, tools used
- `general`: Miscellaneous facts

---

## 💾 Redis Memory View

Inspect stored memory using `redis-cli`:

```bash
redis-cli
> keys user:user_124:memory:*
> smembers user:user_124:memory:profile
```

## 🏃‍➡️Run this Project

1. Clone the Repository

```bash
git clone https://github.com/your-username/personalized-chatbot.git
cd personalized-chatbot
```
2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Required Packages

```bash
pip install -r requirements.txt
```

4. Set Up Your Gemini API Key

Create .env file and set your credentials:
```bash
GEMINI_API_KEY = "your-api-key"
```

5. Start Redis Server

If Redis is not installed:
```bash
# On Ubuntu
sudo apt update
sudo apt install redis
redis-server
```

6. Start Backend (FastAPI):

```bash
uvicorn main:app --reload
```

7. Start Frontend (Streamlit):

```bash
streamlit run streamlit_app.py
```

## 👨‍💻 Author

Fasi Tahir

---




