import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os

st.set_page_config(page_title="NusaBot - Travel Assistant", page_icon="🌴", layout="centered")
st.title("🌴 NusaBot: AI Travel Guide Indonesia")
st.caption("Tanya saya tentang destinasi liburan, kuliner lokal, atau rute perjalanan di Indonesia!")

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("AIzaSyD8GGXwacqvBqQQMttFYRtLO5nk6QFgmVM", type="password")
    st.markdown("[Dapatkan API Key di Google AI Studio](https://aistudio.google.com/)")
    st.divider()
    st.write("💡 **Fitur Utama:**")
    st.write("- Memori Kontekstual")
    st.write("- Spesialis Pariwisata RI")
    st.write("- Gaya Bahasa Santai")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo Kak! Aku NusaBot 🌴. Rencana mau liburan ke mana nih? Gunung, pantai, atau kulineran kota?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Misal: Rekomendasikan pantai sepi di Gunung Kidul..."):
    if not api_key:
        st.info("Tolong masukkan API Key di sidebar terlebih dahulu ya, Kak!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    template = """Kamu adalah NusaBot, asisten travel pariwisata Indonesia yang ramah, antusias, dan menggunakan bahasa Indonesia yang santai (gunakan kata 'Aku' dan 'Kakak').
    Pengetahuanmu berfokus pada destinasi wisata, kuliner, budaya, dan tips traveling di Indonesia.
    Jika user bertanya di luar topik traveling atau pariwisata, tolak dengan sopan dan arahkan kembali ke topik liburan.
    
    Riwayat Obrolan:
    {history}
    
    User: {input}
    NusaBot:"""
    
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, temperature=0.7)
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=False,
        memory=st.session_state.memory
    )

    with st.spinner("NusaBot sedang mencari info terbaik... 🧭"):
        try:
            response = conversation.predict(input=prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
