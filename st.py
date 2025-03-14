import streamlit as st
import requests
import time

# Page configuration
st.set_page_config(page_title="Audio & Text API", layout="centered")

# Custom CSS for modern styling
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #105a8a;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #ddd;
            padding: 10px;
        }
        .stFileUploader>div>div>div>button {
            background-color: #1f77b4 !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎵 Upload Audio & Text for Processing")

uploaded_audio = st.file_uploader("🎙️ Upload an audio file", type=["mp3", "wav", "ogg"], help="Supported formats: MP3, WAV, OGG")
user_text = st.text_input("✍️ Enter text", placeholder="Type your text here...")

if st.button("🚀 Submit"):
    if uploaded_audio and user_text:
        with st.spinner("🔄 Processing... Please wait!"):
            time.sleep(1.5)  # Simulating processing delay
            files = {"audio": uploaded_audio.getvalue()}
            data = {"text": user_text}
            
            try:
                response = requests.post("http://18.222.108.147:5000/generate", files=files, data=data)
                
                if response.status_code == 200:
                    st.success("✅ Successfully processed!")
                    st.audio(response.content, format="audio/mp3")
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.reason}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Request failed: {e}")
    else:
        st.warning("⚠️ Please upload an audio file and enter text.")