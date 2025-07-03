import streamlit as st
import requests

# --- CONFIG ---
API_URL = "http://localhost:8000/chat/"
USER_ID = "user_123"  # In real apps, use session or login

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- PAGE SETUP ---
st.set_page_config(page_title="Smart Chatbot", page_icon="🤖")
st.title("🤖 Memory-Enhanced Chatbot")

# --- INPUT FORM ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submitted = st.form_submit_button("Send")

# --- SEND MESSAGE ---
if submitted and user_input.strip() != "":
    # Append to local history (UI only)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Call FastAPI backend
    try:
        res = requests.post(API_URL, json={"user_id": USER_ID, "message": user_input})
        res.raise_for_status()
        reply = res.json()["response"]
    except Exception as e:
        reply = f"Error: {e}"

    # Store assistant reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# --- DISPLAY CHAT ---
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
