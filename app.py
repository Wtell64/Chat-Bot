import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/chat"

st.title("Deepp AI Chatbot 🤖")

# Session icin state yaratmak
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chati gosterme (sira sira gozukmesi icin)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat mesaj almak icin
if prompt := st.chat_input("Ask me anything..."):
    # mesaj yazilinca yollanmasi icin
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # mesaji chat stateine eklemek icin
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI cevap almak icin
    try:
        response = requests.post(API_URL, json={"message": prompt})
        if response.status_code == 200:
            bot_response = response.json().get("response", "")
        else:
            bot_response = f"Error: {response.status_code}"
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    # Bot cevabini eklemek icin
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Bot cevabini eklemek icin
    st.session_state.messages.append({"role": "assistant", "content": bot_response})