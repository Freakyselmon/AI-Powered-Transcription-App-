import os
import whisper
import streamlit as st
import tempfile
import json

# ✅ Ensure this is the first Streamlit command
st.set_page_config(page_title="AI-Powered Transcriber", page_icon="🎙️", layout="wide")

# Load the Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base")  # Change to "tiny" for a faster model

model = load_model()

# Function to transcribe a file
def transcribe_audio(file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return f"❌ Error: {e}"

# Custom CSS for better styling
st.markdown(
    """
    <style>
        .main {background-color: #f8f9fa;}
        .stFileUploader {border: 2px dashed #3498db; padding: 15px; border-radius: 10px;}
        .stButton>button {background-color: #3498db; color: white; font-size: 18px; padding: 10px; border-radius: 8px;}
        .stDownloadButton>button {background-color: #2ecc71; color: white; font-size: 18px; padding: 10px; border-radius: 8px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and UI Layout
st.title("🎙️ AI-Powered Media Transcriber")
st.write("Upload an **audio or video file**, and get an **instant transcription!**")

uploaded_files = st.file_uploader(
    "Drag and drop or browse files",
    type=["mp3", "wav", "mp4", "mkv", "avi"],
    accept_multiple_files=True
)

if uploaded_files:
    output_transcriptions = {}

    for uploaded_file in uploaded_files:
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            st.markdown(f"#### 🔄 Transcribing: {uploaded_file.name}...")
            transcription = transcribe_audio(temp_file_path)

            # Display transcription result
            with st.expander(f"📜 **Transcription: {uploaded_file.name}**", expanded=True):
                st.write(transcription)

            # Save transcriptions in a dictionary for downloading
            output_transcriptions[uploaded_file.name] = transcription

        except Exception as e:
            st.error(f"⚠️ Error processing {uploaded_file.name}: {e}")

        finally:
            # Ensure temp file is deleted
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    # Provide download options for transcriptions
    st.success("✅ **Transcription Completed!** Download your transcript below:")

    # Save transcriptions to a text file
    text_output = "\n\n".join([f"{file}:\n{trans}" for file, trans in output_transcriptions.items()])
    json_output = json.dumps(output_transcriptions, indent=4)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📄 Download TXT", text_output, "transcription.txt", "text/plain")
    with col2:
        st.download_button("📂 Download JSON", json_output, "transcription.json", "application/json")

st.write("💡 **Tip:** Use high-quality audio for better transcriptions!")

#streamlit run app.py
