# import streamlit as st
# import requests
# import base64

# st.set_page_config(page_title="Voice Cloner", layout="centered")

# # ---------- Global Styling ----------
# st.markdown("""
#     <style>
#     /* Dark mode background */
#     .stApp {
#         background-color: #0f1117;
#         color: #fff;
#     }
#     /* Center title */
#     .main-title {
#         text-align: center;
#         font-size: 3rem;
#         font-weight: 700;
#         color: #d6d6d6;
#         margin-top: 2rem;
#     }
#     .subtitle {
#         text-align: center;
#         color: #aaa;
#         margin-bottom: 2rem;
#     }
#     /* Spinner animation */
#     .loader {
#         border: 8px solid #333;
#         border-top: 8px solid #00ffcc;
#         border-radius: 50%;
#         width: 60px;
#         height: 60px;
#         animation: spin 1s linear infinite;
#         margin: 30px auto;
#     }
#     @keyframes spin {
#         0% { transform: rotate(0deg); }
#         100% { transform: rotate(360deg); }
#     }
#     /* Expand text area */
#     .stTextArea textarea {
#         min-height: 250px !important;
#         padding: 1rem;
#         resize: vertical;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ---------- Sidebar Inputs ----------
# st.sidebar.title("🎛️ Controls")
# ref_audio = st.sidebar.file_uploader("📁 Upload reference audio", type=["mp3", "wav", "ogg", "flac", "m4a", "aac", "wma"])
# gen_text = st.sidebar.text_area("✍️ Text to generate (required)")

# # Add a button to toggle extra settings
# extra_settings = st.sidebar.checkbox("🔧 Extra Settings")

# # Only show speed control if "Extra Settings" is enabled
# if extra_settings:
#     speed = st.sidebar.slider("⏩ Speech speed", min_value=0.1, max_value=2.0, value=0.9, step=0.1)
# else:
#     speed = None

# generate_button = st.sidebar.button("🚀 Generate Voice")

# # ---------- Main UI ----------
# st.markdown('<div class="main-title">🎙️ Voice Cloner</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Clone a voice from a sample audio and custom text</div>', unsafe_allow_html=True)

# # Create a placeholder for the loader
# loader_placeholder = st.empty()

# if generate_button:
#     if not ref_audio or not gen_text.strip():
#         st.error("❗ Please upload an audio file and enter text.")
#     else:
#         # Show loader immediately
#         with loader_placeholder:
#             st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
        
#         # Prepare the files
#         files = {
#             'ref_audio': (ref_audio.name, ref_audio, 'audio/mpeg'),
#         }

#         # Prepare the data
#         data = {'gen_text': gen_text}
#         if extra_settings and speed != 0.9:
#             data['speed'] = str(speed)

#         try:
#             response = requests.post("http://98.84.143.182:5000/clone", files=files, data=data)

#             # Clear loader before showing results
#             loader_placeholder.empty()

#             if response.status_code == 200:
#                 audio_bytes = response.content
#                 b64_audio = base64.b64encode(audio_bytes).decode()
#                 st.success("✅ Voice generated successfully!")

#                 st.markdown(f"""
#                     <audio autoplay controls style="width: 100%; margin-top: 1rem;">
#                         <source src="data:audio/wav;base64,{b64_audio}" type="audio/wav">
#                         Your browser does not support the audio element.
#                     </audio>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.error(f"API Error: {response.status_code} — {response.text}")

#         except Exception as e:
#             loader_placeholder.empty()
#             st.error(f"⚠️ Request failed: {e}")

import streamlit as st
import requests
import base64

st.set_page_config(page_title="Voice Cloner", layout="centered")

# ---------- Global Styling ----------
st.markdown("""
    <style>
    /* Dark mode background */
    .stApp {
        background-color: #0f1117;
        color: #fff;
    }
    /* Center title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #d6d6d6;
        margin-top: 2rem;
    }
    .subtitle {
        text-align: center;
        color: #aaa;
        margin-bottom: 2rem;
    }
    /* Spinner animation */
    .loader {
        border: 8px solid #333;
        border-top: 8px solid #00ffcc;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
        margin: 30px auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    /* Expand text area */
    .stTextArea textarea {
        min-height: 250px !important;
        padding: 1rem;
        resize: vertical;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar Inputs ----------
st.sidebar.title("🎛️ Controls")

# Radio button to select the API
api_choice = st.sidebar.radio("🌐 Select API", ["Spanish language", "English language"])

ref_audio = st.sidebar.file_uploader("📁 Upload reference audio", type=["mp3", "wav", "ogg", "flac", "m4a", "aac", "wma"])
gen_text = st.sidebar.text_area("✍️ Text to generate (required)")

# Add a button to toggle extra settings
extra_settings = st.sidebar.checkbox("🔧 Extra Settings")

# Only show speed control if "Extra Settings" is enabled
if extra_settings:
    speed = st.sidebar.slider("⏩ Speech speed", min_value=0.1, max_value=2.0, value=0.9, step=0.1)
else:
    speed = None

generate_button = st.sidebar.button("🚀 Generate Voice")

# ---------- Main UI ----------
st.markdown('<div class="main-title">🎙️ Voice Cloner</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Clone a voice from a sample audio and custom text</div>', unsafe_allow_html=True)

# Create a placeholder for the loader
loader_placeholder = st.empty()

if generate_button:
    if not ref_audio or not gen_text.strip():
        st.error("❗ Please upload an audio file and enter text.")
    else:
        # Show loader immediately
        with loader_placeholder:
            st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
        
        # Prepare the files
        files = {
            'ref_audio': (ref_audio.name, ref_audio, 'audio/mpeg'),
        }

        # Prepare the data
        data = {'gen_text': gen_text}
        if extra_settings and speed != 0.9:
            data['speed'] = str(speed)

        try:
            # Choose API endpoint based on user selection
            if api_choice == "Spanish language":
                api_url = "http://98.84.143.182:5000/clone"  # Replace with your first API endpoint
            elif api_choice == "English language":
                api_url = "http://98.84.143.182:5001/tts"  # Replace with your second API endpoint

            response = requests.post(api_url, files=files, data=data)

            # Clear loader before showing results
            loader_placeholder.empty()

            if response.status_code == 200:
                audio_bytes = response.content
                b64_audio = base64.b64encode(audio_bytes).decode()
                st.success("✅ Voice generated successfully!")

                st.markdown(f"""
                    <audio autoplay controls style="width: 100%; margin-top: 1rem;">
                        <source src="data:audio/wav;base64,{b64_audio}" type="audio/wav">
                        Your browser does not support the audio element.
                    </audio>
                """, unsafe_allow_html=True)
            else:
                st.error(f"API Error: {response.status_code} — {response.text}")

        except Exception as e:
            loader_placeholder.empty()
            st.error(f"⚠️ Request failed: {e}")