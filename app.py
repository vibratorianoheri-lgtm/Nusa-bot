import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="NusaBot - Travel Assistant", page_icon="🌴")
st.title("🌴 NusaBot: AI Travel Guide Indonesia")
st.caption("Solusi cerdas rencana liburanmu!")

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")
    st.info("Dapatkan API Key di Google AI Studio.")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo Kak! Aku NusaBot 🌴. Mau rencana liburan ke mana nih?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Tanya destinasi, kuliner, atau tips travel..."):
    if not api_key:
        st.warning("Silakan masukkan API Key terlebih dahulu di sidebar kiri!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    template = """Kamu adalah NusaBot, asisten travel Indonesia yang ramah. 
    Gunakan bahasa Indonesia yang santai. Jawablah hanya seputar pariwisata Indonesia.
    
    Riwayat Percakapan:
    {history}
    
    User: {input}
    NusaBot:"""
    
    prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)
    
    try:
      llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", # <--- Gunakan nama lengkap ini
            google_api_key=api_key,
            temperature=0.7
        )
        
        conversation = ConversationChain(
            prompt=prompt_template,
            llm=llm,
            memory=st.session_state.memory
        )

        with st.spinner("NusaBot sedang berpikir..."):
            response = conversation.predict(input=prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)
            
    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {str(e)}")
