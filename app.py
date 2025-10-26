# app.py (Msingo wa Streamlit Chatbot)

import streamlit as st
import os
from google import genai
from google.genai.errors import APIError

# --- 1. Usanidi wa API Client na Models ---

# Tofauti na Groq, Gemini hutumia genai.Client
# Inapendekezwa kutumia st.secrets kwa usalama zaidi.
# Badilisha 'GEMINI_API_KEY' na jina la ufunguo uliloweka kwenye secrets.toml
# Kama ulifuata maelekezo, jina linapaswa kuwa 'gemini_api_key'
GEMINI_API_KEY_NAME = "gemini_api_key"

# Angalia kama Key ipo, la sivyo toa ujumbe wa onyo
try:
    if GEMINI_API_KEY_NAME in st.secrets:
        # Pata Key kutoka kwa Streamlit Secrets
        API_KEY = st.secrets[GEMINI_API_KEY_NAME]
    else:
        # Tumia API Key ya mfano, na kisha utoe onyo
        API_KEY = "AIzaSyD8D5-NrexDxNvCZ4lAh4nEi9T5A9HC9ns"
        st.error("❌ Kosa: Haujaweka Gemini API Key kwenye faili ya .streamlit/secrets.toml.")
        st.stop() # Sitisha programu isijaribu kuunganisha bila Key

    @st.cache_resource
    def initialize_gemini_client(api_key):
        return genai.Client(api_key=api_key) 
            
    client = initialize_gemini_client(API_KEY)

except Exception as e:
    st.error(f"Kosa kubwa wakati wa kuunganisha na Gemini: {e}")
    st.stop() # Sitisha programu ikiwa uunganisho umefeli

# Usanidi wa Model na System Prompt
GEMINI_MODEL = "gemini-2.5-flash" 

SYSTEM_PROMPT = """Wewe ni Aura, msaidizi wa huduma kwa wateja kwa biashara ya mtandaoni iitwayo 'SmartTz'. 
Jukumu lako ni kutoa majibu ya haraka, sahihi, na ya kirafiki kwa lugha ya Kiswahili fasaha. 
Jibu maswali yote kwa lugha ya Kiswahili, hata kama maswali yameulizwa kwa lugha nyingine. 
Weka jibu lako fupi, wazi, na la kusaidia. Jibu kwa heshima na uepuke kuongea kuhusu maswala 
ambayo si ya biashara. Anza kila jibu kwa salamu fupi ya kirafiki au Emoji moja inayofaa.
"""

# --- 2. Usanidi wa Streamlit UI na Logic ---

st.set_page_config(page_title="Aura Chatbot (Gemini Powered)", page_icon="✨")
st.title("Aura, Msaidizi wa SmartTz ✨")
st.caption("Uliza chochote kuhusu bidhaa, maagizo, au usaidizi wetu.")

# Anzisha historia ya mazungumzo
if "messages" not in st.session_state:
    st.session_state.messages = []

# Onyesha historia ya mazungumzo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kichakata cha kuingiza maoni ya mtumiaji
if prompt := st.chat_input("Nisaidie na..."):
    # Ongeza maoni ya mtumiaji kwenye historia
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tayarisha ujumbe kwa ajili ya API ya Gemini
    # Gemini hutumia 'contents' ambayo hubeba historia yote ya mazungumzo
    # na inajumuisha jukumu ('role') la kila ujumbe.
    gemini_contents = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
        for m in st.session_state.messages
    ]

    # 3. Piga API call kwa Gemini
    try:
        with st.chat_message("assistant"):
            with st.spinner("Aura anajibu..."):
                
                # Gemini hutumia 'generate_content' kwa chat na system instruction
                chat_completion = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=gemini_contents,
                    config={
                        "system_instruction": SYSTEM_PROMPT, 
                        "temperature": 0.7,
                    }
                )
                
                response = chat_completion.text
                st.markdown(response)

    except APIError as e:
        # Simamia makosa ya Gemini API (kama API Key Invalid au Rate Limit)
        response = f"Nakuomba radhi Abdulkarim, mfumo wa Gemini una changamoto kwa sasa (API Error). Tafadhali hakikisha Key yako ni sahihi na hukuweka 'Cloud Billing'. Kosa hasa: {e}"
        st.markdown(response)
        
    except Exception as e:
        # Simamia makosa mengine ya mfumo
        response = f"Samahani, kumetokea kosa lisilotarajiwa: {e}" 
        st.markdown(response)


    # 4. Ongeza jibu la Aura kwenye historia ya mazungumzo ya Streamlit
    st.session_state.messages.append({"role": "assistant", "content": response})

