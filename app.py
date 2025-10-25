import streamlit as st
from groq import Groq
import os

# Basic UI
st.title("🤖 Aura — Customer Service AI")
st.write("Karibu! Uliza chochote kuhusu huduma zetu 📞✨")

# Initialize Groq client using the environment variable
client = Groq(api_key=os.getenv("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"))

# Chat input
user_input = st.text_input("✍️ Andika ujumbe wako hapa:")

if user_input:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are Aura, a friendly customer service assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    
    reply = response.choices[0].message["content"]
    st.success(reply)
