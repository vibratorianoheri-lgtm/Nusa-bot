import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NusaBot Debug Version", page_icon="🌴")
st.title("🌴 NusaBot: AI Travel Guide")

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password", key="api_input")
    
    if api_key:
        st.success("API Key terdeteksi! Siap digunakan.")
    else:
        st.warning("Menunggu API Key...")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
    "models/gemini-2.5-flash-lite",
    generation_config={
        "max_output_tokens": 200
    }
)
        
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            st.session_state.messages = []
            st.session_state.messages.append({"role": "assistant", "content": "Halo! NusaBot sudah aktif. Mau tanya apa hari ini?"})
            
    except Exception as e:
        st.error(f"Gagal koneksi ke Google: {e}")

if "messages" in st.session_state:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ketik pesan di sini..."):
    if not api_key:
        st.error("Masukkan API Key di sidebar dulu ya!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.spinner("Berpikir..."):
                response = st.session_state.chat.send_message(prompt)
                full_response = response.text
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                with st.chat_message("assistant"):
                    st.markdown(full_response)
        except Exception as e:
            st.error(f"Waduh, ada error pas jawab: {e}")
