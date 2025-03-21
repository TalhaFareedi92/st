import streamlit as st
import requests
import time

# API Endpoints
API_URL = "http://3.145.183.202:5050/openvoice/generate"
STATUS_URL = "http://3.145.183.202:5050/openvoice/files/status/"
RESULT_URL = "http://3.145.183.202:5050/openvoice/files/result/"

# Streamlit UI Configuration
st.set_page_config(page_title="AI TTS Processor", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #4A90E2;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("AI TTS Processor")
    st.markdown("Upload a voice file and text to process.")
    menu_option = st.radio("Navigation", ["Upload & Process", "Check Status", "Download Voice"])

# Main Content
st.markdown("<div class='main-header'>Text-to-Speech Processing Using Open Voice</div>", unsafe_allow_html=True)

if menu_option == "Upload & Process":
    st.subheader("Step 1: Upload Voice and Text")
    with st.form("tts_form"):
        text_input = st.text_area("Enter text:")
        uploaded_file = st.file_uploader("Upload voice file", type=["wav", "mp3", "ogg"])
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if not text_input or not uploaded_file:
            st.error("Please provide both text and a voice file.")
        else:
            with st.spinner("Uploading and processing..."):
                files = {"audio": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                data = {"text": text_input}

                try:
                    response = requests.post(API_URL, files=files, data=data)
                    time.sleep(2)

                    if response.status_code == 202:
                        try:
                            response_json = response.json()
                            file_id = response_json.get("file_id")
                            if file_id:
                                st.session_state["file_id"] = file_id
                                st.success("Your request has been queued successfully!")
                                st.json(response_json)
                            else:
                                st.error("File ID not found in response.")
                        except requests.exceptions.JSONDecodeError:
                            st.error("Unexpected response format from the API.")
                            st.text(response.text)  # Display raw response for debugging
                    else:
                        st.error(f"Failed to process request. Status Code: {response.status_code}")
                        st.text(response.text)  # Display raw response for debugging

                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")

elif menu_option == "Check Status":
    st.subheader("Step 2: Check File Processing Status")
    file_id_input = st.text_input("Enter File ID:", st.session_state.get("file_id", ""))
    
    if st.button("Check Status"):
        if not file_id_input:
            st.error("Please enter a valid file ID.")
        else:
            with st.spinner("Checking status..."):
                try:
                    status_response = requests.get(f"{STATUS_URL}{file_id_input}")
                    time.sleep(2)

                    if status_response.status_code == 200:
                        try:
                            status_json = status_response.json()
                            status = status_json.get("status")
                            st.success(f"Status: {status}")
                            st.json(status_json)

                            if status == "completed":
                                st.session_state["status"] = "completed"
                                st.session_state["file_id"] = file_id_input  # Save the latest completed file ID
                        except requests.exceptions.JSONDecodeError:
                            st.error("Unexpected response format.")
                            st.text(status_response.text)  # Show raw response
                    else:
                        st.error(f"Failed to fetch status. Status Code: {status_response.status_code}")
                        st.text(status_response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")

elif menu_option == "Download Voice":
    st.subheader("Step 3: Download Processed Voice File")
    file_id_input = st.text_input("Enter File ID:", st.session_state.get("file_id", ""))
    
    if st.button("Get Cloned Voice"):
        if not file_id_input:
            st.error("Please enter a valid file ID.")
        else:
            with st.spinner("Fetching processed voice file..."):
                try:
                    result_response = requests.get(f"{RESULT_URL}{file_id_input}", stream=True)
                    time.sleep(2)

                    if result_response.status_code == 200:
                        output_file = f"cloned_voice_{file_id_input}.wav"
                        with open(output_file, "wb") as f:
                            for chunk in result_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        st.success("Cloned voice file downloaded successfully!")
                        st.audio(output_file, format="audio/wav")
                    else:
                        st.error(f"Failed to fetch cloned voice. Status Code: {result_response.status_code}")
                        st.text(result_response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")
