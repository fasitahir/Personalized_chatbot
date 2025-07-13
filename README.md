# 🤖 Memory-Enhanced Personalized Chatbot

A smart chatbot that remembers who you are! This project uses Google Gemini API, FastAPI, Redis, and Streamlit to create a personalized chat experience with both **short-term memory** (chat history) and **long-term memory** (stored facts about the user).

---

## 📌 Features

- 🧠 **Memory-aware assistant** — stores and recalls user details like name, location, preferences, projects.
- 🔁 **Short-term memory** — remembers recent conversation context (last 5–10 messages).
- 💾 **Long-term memory** — uses Redis to persist important facts.
- ⚡ **FastAPI backend** — serves a structured Gemini-powered LLM response.
- 🎯 **Streamlit frontend** — clean, responsive user interface.
- 🛠️ **Fact extraction** — structured personal facts are categorized and stored.

---

## 🧠 How It Works

### 🔹 Short-Term Memory
Stored in memory as recent messages. Injected into prompt to keep conversational context.

### 🔹 Long-Term Memory (Redis)
Facts are extracted by Gemini from conversations and stored under:

```
user:<user_id>:memory:<category>
```

Categories include:
- `profile`: Name, location, age, etc.
- `projects`: User’s work or academic projects
- `preferences`: Likes, dislikes, tools used
- `general`: Unstructured facts

---

## 💾 Redis Memory View

To inspect what's stored:

```bash
redis-cli
> keys user:user_124:memory:*
> smembers user:user_124:memory:profile
```

---

## 📁 Project Structure

```
personalized-chatbot/
│
├── main.py              # FastAPI backend with Gemini & memory logic
├── chat_history.py      # Stores recent messages (short-term)
├── memory.py            # Redis interactions (long-term memory)
├── categorize.py        # Determines memory category
├── config.py            # API keys and model config
├── streamlit_app.py     # Streamlit UI
├── requirements.txt     # All dependencies
└── README.md            # This file
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/personalized-chatbot.git
cd personalized-chatbot
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up Your Gemini API Key

Create `.env` file and add:

```python
GEMINI_API_KEY = "your-api-key"
```

### 5. Start Redis Server

If Redis is not installed:

```bash
# Ubuntu
sudo apt update
sudo apt install redis
redis-server
```

Or use Docker:

```bash
docker run -d -p 6379:6379 redis
```

---

## 🚀 Run the Application

### Start Backend (FastAPI):

```bash
uvicorn main:app --reload
```

### Start Frontend (Streamlit):

```bash
streamlit run streamlit_app.py
```

---

## 🧪 Sample Interaction

```text
You: I'm Fasi from Lahore.
Bot: Nice to meet you, Fasi! Lahore is a beautiful city.

Facts extracted:
- Name: Fasi
- Location: Lahore
```

These are stored in Redis and used in future chats.

---

## 🧩 Reducing Repetition

The backend avoids duplicating stored facts by:
- Retrieving existing facts
- Checking if a fact already exists before saving (optional improvement you can add)

---

## ⏱️ Measuring Latency

Each request's latency is printed in milliseconds in the backend logs using:

```python
start = time.perf_counter()
...
end = time.perf_counter()
print(f"Latency: {round((end - start) * 1000, 2)} ms")
```

---

## 🔮 Future Enhancements

- Semantic memory search with FAISS or LightRAG
- Edit/delete memory entries from UI
- Real-time message streaming
- User authentication
- Support for OpenAI / Claude / Cohere

---

## 📄 License

MIT License

---

## 🙌 Acknowledgements

- [Google Gemini API](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Redis](https://redis.io/)
- [Streamlit](https://streamlit.io/)

---

## 👨‍💻 Author

Fasi Tahir – [@FasiTahir](https://github.com/FasiTahir)
