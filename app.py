# File: app.py

import streamlit as st
import whisper
import os
import uuid

model = whisper.load_model("small")

stream_button_styles = """
<style>
    header { display: none !important; }
</style>
"""

page_styles = """
<style>
    h1 { font-size: 2rem; font-weight: 700; }
    h2 { font-size: 1.7rem; font-weight: 600; }
    .timestamp { color: gray; font-size: 0.9rem; }
</style>
"""

page_title = "Using OpenAI Whisper to Transcribe Podcasts"

page_description = "A demo showcasing the use of OpenAI Whisper to accurately and efficiently convert spoken content from podcasts into written text."

koyeb_box = "To deploy Whisper within minutes, <a href=\"https://koyeb.com/ai\">Koyeb GPUs</a> provide the easiest and most efficient way. Koyeb offers a seamless platform for deploying AI models, leveraging high-performance GPUs to ensure fast and reliable transcriptions."

step_1 = "1. Upload Podcast"

step_2 = "2. Invoke OpenAI Whisper to transcribe podcast 👇🏻"

step_3 = "3. Transcription &nbsp; 🎉"

def unsafe_html(tag, text):
    return st.markdown(f"<{tag}>{text}</{tag}>", unsafe_allow_html=True)

# Generate transcription of each segment
def timestamp_html(segment):
    return f'<span class="timestamp">[{segment["start"]:.2f} - {segment["end"]:.2f}]</span> {segment["text"]}'

# Transcribe an audio file
def transcribe_audio(audio_file_path):
    return model.transcribe(audio_file_path)

# Write the audio file on server
def write_audio(audio_file):
    unique_filename = f"{uuid.uuid4()}_{audio_file.name}"
    with open(unique_filename, "wb") as f:
        f.write(audio_file.read())
    return unique_filename

def main():
    # Set title for the page
    st.set_page_config(page_title=page_title, layout="centered")
    # Inject hide buttons CSS
    st.markdown(stream_button_styles, unsafe_allow_html=True)
    # Inject page CSS
    st.markdown(page_styles, unsafe_allow_html=True)
    # Create a H1 heading on the page
    st.title(page_title)
    unsafe_html("h2", page_description)
    unsafe_html("p", koyeb_box)
    audio_file = st.file_uploader(step_1, type=["mp3", "mp4", "wav", "m4a"])
    if audio_file:
        # If file is received
        # Write the file on the server
        audio_file_path = write_audio(audio_file)
        # Show next step
        unsafe_html("small", step_2)
        if st.button("Transcribe"):
            # Get the transcription
            transcript_text = transcribe_audio(audio_file_path)
            unsafe_html("small", step_3)
            # Showcase the transcription
            for segment in transcript_text["segments"]:
                unsafe_html("div", timestamp_html(segment))
            # Clean up the saved audio file
            os.remove(audio_file_path)

if __name__ == "__main__":
    main()