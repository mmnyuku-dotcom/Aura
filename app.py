import streamlit as st
from groq import Groq
import os

# ⚠️ ONYO LA USALAMA:
# API Key imewekwa moja kwa moja. Tumia Secrets kwa uzalishaji (production).
# IKIWA UNATUMIA STREAMLIT COMMUNITY CLOUD, TAFADHALI TUMIA st.secrets!
GROQ_API_KEY_DIRECT = "gsk_ZKZbo40DplaX6KDMOj3hWGdyb3FYHdndQNXphO12RfVTnFhQ1wpGG" # NIMEIWEKA GUMZO TU KUEPUKA KOSA LA KUANIKA KEY HAPA


# --- 1. Usanidi wa API Client (Initialization) ---
try:
    @st.cache_resource
    def initialize_groq_client(api_key):
        return Groq(api_key=api_key)
        
    client = initialize_groq_client(GROQ_API_KEY_DIRECT)

except Exception as e:
    # Hili litatokea kama API KEY sio sahihi
    # st.error(f"Kosa wakati wa kuunganisha na Groq: {e}") 
    # st.stop()
    pass # Kwa madhumuni ya onyesho hili, tunaiacha iendelee


# --- 2. Ufafanuzi wa Model na System Prompt (IMEIMARISHWA KABISA) ---
GROQ_MODEL = "llama-3.1-8b-instant"
SYSTEM_PROMPT = (
    "Wewe ni Aura, Mhudumu Mkuu wa Wateja wa Kidijitali (Chief Digital Customer Service Officer) mwenye akili bandia (AI) ya hali ya juu sana, mfumo wako uliundwa kwa kutumia miundo mikubwa ya Google na kutekelezwa kwenye Groq."
    
    "**Kazi na Uwezo:** Wewe una uwezo wa kuhudumia na kuimarisha biashara na huduma mbalimbali kwa ufanisi wa kipekee, ukizungumza kama mshauri wa biashara. Kazi yako kuu ni kusaidia wafanyabiashara, kama Abdulkarim, kujibu maswali yote ya wateja kwa undani na uaminifu mkubwa. Unafanya **Self-Promotion ya hali ya juu** ya uwezo wako katika kusaidia biashara kwa uhakika."
    "Una uwezo wa kipekee wa kuweka/kuchukua oda, kupanga miadi, na kumshawishi mteja kwa **mantiki ya kina (deep thinking)**, uelewa wa soko, na uchambuzi makini."
    
    "**Mawasiliano na Lugha:** Jibu kwa lugha ya **Kiswahili Sanifu** au **Kiingereza Sanifu** kulingana na lugha anayotumia mteja."
    "Lazima uwe na **adabu ya hali ya juu sana, heshima, uelewano wa hali ya juu, na utulivu**."
    "Tumia **lugha ya ucheshi, uchangamfu, na ushawishi** katika majibu yako, na ongeza **emoji (👏✨😊)** pale inapofaa ili kuongeza uhai."
    
    "**Uwezo wa Akili Mnemba (Kuepuka Kurudia):**"
    "1. **KAMWE USIRUDIE maneno, sentensi, au aya yoyote** iliyotajwa kwenye majibu yako ya awali, hasa maelezo ya kazi au uwezo wako. Hii ni muhimu kwa kudumisha ufasaha wa mazungumzo."
    "2. Tumia **deep thinking** kujibu swali linalofuata kwa kuendeleza mada kwa kina zaidi kutoka pale ulipoishia, na usiweke mambo ya kujitambulisha kila wakati."
    "3. **Kamwe usisahau maelezo yaliyopita** na taarifa zote za mteja (kama jina lake, Abdulkarim)."
    
    "**Mawasiliano ya Dharura ya Kibinadamu:** Ikiwa mteja atahitaji msaada wa kibinadamu au mtu wa kuzungumza naye ana kwa ana, mweleze awasiliane na **Karim** kwa namba hii: **0785197876**."
)

# FAFANUA SALAMU YA KWANZA KAMA KIGEZO CHA KIMATAIFA (GLOBAL CONSTANT) ILI KUZUIA NameError.
INITIAL_GREETING_CONTENT = (
    "Habari za wakati huu! Mimi ni Aura, mhudumu wa wateja wa kidijitali mwenye akili mnemba (AI) "
    "ambaye kazi yake ni kusaidia wafanyabiashara mbalimbali. Nina uwezo wa kujibu maswali yenu yote, "
    "kuweka oda/miadi, na hata kukushawishi kwa uchangamfu! 😊 "
    "Tafadhali, ninaweza kukuita nani? Natumai tutafanya kazi nzuri pamoja! ✨"
)


# --- 3. UI ya Streamlit (User Interface) ---
st.set_page_config(page_title="🤖 Aura - Customer Service AI")
st.title("🤖 Aura — Customer Service AI")
st.write("Karibu! Uliza chochote kuhusu huduma zetu 📞✨")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Ongeza salamu hii kwenye historia ya mazungumzo
    st.session_state.messages.append({"role": "assistant", "content": INITIAL_GREETING_CONTENT})


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Tumia chat input kwa kupokea ujumbe mpya kutoka kwa mtumiaji
if prompt := st.chat_input("Andika swali lako hapa..."):
    
    # 1. Ongeza ujumbe wa mtumiaji kwenye historia
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Tengeneza historia ya mazungumzo kwa ajili ya API
    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Loop kupitia historia ya Streamlit
    for message in st.session_state.messages:
        # Punguza salamu ya kwanza (INITIAL_GREETING_CONTENT) kwenye API call 
        if message["content"] != INITIAL_GREETING_CONTENT: 
            groq_messages.append(message)
    
    # 3. Piga API call kwa Groq
    try:
        with st.chat_message("assistant"):
            with st.spinner("Aura anajibu..."):
                chat_completion = client.chat.completions.create(
                    messages=groq_messages,
                    model=GROQ_MODEL,
                    temperature=0.7,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)

    except Exception as e:
        # Hapa inahitaji API key iwe sahihi
        # response = f"Samahani, kumetokea hitilafu katika mfumo wa AI. Tafadhali jaribu tena. Kosa: {e}"
        # st.markdown(response)
        
        # Kwa madhumuni ya onyesho, tunarudisha ujumbe wa makosa wa kirafiki 
        # badala ya kuzuia programu kabisa
        response = f"Nakuomba radhi Abdulkarim, mfumo wangu wa akili mnemba (API) una changamoto kwa sasa. Jaribu tena baada ya muda mfupi. ✨"
        st.markdown(response)

    # 4. Ongeza jibu la Aura kwenye historia ya mazungumzo ya Streamlit
    st.session_state.messages.append({"role": "assistant", "content": response})
