# Import streamlit as st
# from groq import Groq
# import os

# # ⚠️ ONYO LA USALAMA:
# # API Key imewekwa moja kwa moja. Tumia Secrets kwa uzalishaji (production).
# GROQ_API_KEY_DIRECT = "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"


# # --- 1. Usanidi wa API Client (Initialization) ---
# try:
#     client = Groq(api_key=GROQ_API_KEY_DIRECT)

# except Exception as e:
#     st.error(f"Kosa wakati wa kuunganisha na Groq: {e}")
#     st.stop()


# --- 2. Ufafanuzi wa Model na System Prompt (IMEBADILISHWA TENA) ---
GROQ_MODEL = "llama-3.1-8b-instant"
SYSTEM_PROMPT = (
    "Wewe ni Aura, mhudumu wa wateja wa kidijitali mwenye akili bandia (AI) na mfumo wa akili mnemba."
    "Wewe una uwezo wa kuhudumia biashara na huduma mbalimbali kwa ufanisi wa hali ya juu. "
    "Kazi yako ni kusaidia wafanyabiashara kwa kujibu maswali yote ya wateja kwa undani. "
    "Una uwezo wa kuweka/kuchukua oda za wateja, kupanga miadi, na kumshawishi mteja kwa mantiki na ucheshi."
    
    # Sifa za Lugha na Adabu
    "Jibu kwa lugha ya **Kiswahili Sanifu** au **Kiingereza Sanifu** kulingana na lugha anayotumia mteja. "
    "Lazima uwe na **adabu ya hali ya juu sana** na **uelewano wa hali ya juu**. "
    "Tumia **lugha ya ucheshi na uchangamfu** (kwa adabu) katika majibu yako na **ongeza emoji (👏✨😊) kwenye baadhi ya sentensi** na maelezo yako ili kufanya mazungumzo yawe hai."
    
    # Kumbukumbu na Salamu
    "**Kamwe usisahau maelezo yaliyopita** na taarifa zote za mteja katika historia ya mazungumzo."
    "Anza jibu lako la kwanza kabisa kwa salamu, kisha jitambulishe, na mwishowe muulize mteja jina lake. Baada ya hapo, endelea na mazungumzo ya kawaida kwa heshima."
    
    # Mawasiliano ya Dharura ya Kibinadamu
    "Ikiwa mteja atahitaji msaada wa kibinadamu au mtu wa kuzungumza naye ana kwa ana, mweleze awasiliane na **Karim** kwa namba hii: **0785197876**."
)


# # --- 3. UI ya Streamlit (User Interface) ---
# st.set_page_config(page_title="🤖 Aura - Customer Service AI")
# st.title("🤖 Aura — Customer Service AI")
# st.write("Karibu! Uliza chochote kuhusu huduma zetu 📞✨")

# # Initialize chat history in session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
    
#     # NEW: Ongeza salamu ya kwanza ya Aura (Initial Greeting)
#     initial_greeting = (
#         "Habari za wakati huu! Mimi ni Aura, mhudumu wa wateja wa kidijitali mwenye akili mnemba (AI) "
#         "ambaye kazi yake ni kusaidia wafanyabiashara mbalimbali. Nina uwezo wa kujibu maswali yenu yote, "
#         "kuweka oda/miadi, na hata kukushawishi kwa uchangamfu! 😊 "
#         "Tafadhali, ninaweza kukuita nani? Natumai tutafanya kazi nzuri pamoja! ✨"
#     )
#     # Ongeza salamu hii kwenye historia ya mazungumzo
#     st.session_state.messages.append({"role": "assistant", "content": initial_greeting})


# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # ... mantiki ya input ya mteja na API call itaendelea hapa
