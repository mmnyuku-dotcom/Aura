import streamlit as st
from groq import Groq
import os

# ⚠️ ONYO LA USALAMA:
# Hii inarekebishwa kulingana na ombi lako la kuingiza API Key moja kwa moja.
# Njia hii haipendekezwi kwa code ya uzalishaji (production code) au code inayowekwa kwenye GitHub
# kwa sababu inaweka wazi ufunguo wako.
GROQ_API_KEY_DIRECT = "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"


# --- 1. Usanidi wa API Client (Initialization) ---
try:
    # Tunatumia ufunguo ulioingizwa moja kwa moja
    client = Groq(api_key=GROQ_API_KEY_DIRECT)

except Exception as e:
    st.error(f"Kosa wakati wa kuunganisha na Groq: {e}")
    st.stop()


# --- 2. Ufafanuzi wa Model na System Prompt ---
GROQ_MODEL = "llama3-8b-8192"
SYSTEM_PROMPT = "Wewe ni Aura, msaidizi rafiki wa huduma kwa wateja. Jibu maswali yote kwa lugha ya Kiswahili, kwa kutumia lugha rahisi na yenye heshima. Lengo lako ni kutoa majibu sahihi na kusaidia kwa furaha."


# --- 3. UI ya Streamlit (User Interface) ---
st.set_page_config(page_title="🤖 Aura - Customer Service AI")
st.title("🤖 Aura — Customer Service AI")
st.write("Karibu! Uliza chochote kuhusu huduma zetu 📞✨")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- 4. Kazi ya Kutuma Ombi la Chat ---
def get_groq_response(prompt):
    """Hutuma ujumbe kwa Groq API na kurudisha jibu."""
    
    # Jenga orodha ya ujumbe ikijumuisha system prompt na historia ya chat
    messages_for_api = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    # Ongeza ujumbe wote wa sasa kutoka kwa session state, ukiondoa system prompt
    for msg in st.session_state.messages:
        messages_for_api.append(msg)
    
    # Ongeza ujumbe wa mtumiaji wa sasa
    messages_for_api.append({"role": "user", "content": prompt})

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages_for_api,
            temperature=0.7 # Unaweza kurekebisha hii
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Samahani, kosa limetokea wakati wa kupata jibu: {e}"


# --- 5. Eneo la Kuandika Ujumbe (Chat Input) ---
if user_input := st.chat_input("✍️ Andika ujumbe wako hapa:"):
    
    # 1. Onyesha ujumbe wa mtumiaji
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Pata jibu kutoka kwa AI
    with st.chat_message("assistant"):
        with st.spinner('Aura inatafakari...'):
            response = get_groq_response(user_input)
            st.markdown(response)

    # 3. Hifadhi jibu la AI kwenye historia
    st.session_state.messages.append({"role": "assistant", "content": response})

