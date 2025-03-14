import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

import streamlit as st

st.logo(
  "logo.png",
  size="medium",
  link="https://platform.openai.com/docs",
)

st.title("Transcription with Whisper")

audio_value = st.audio_input("record a voice message to transcribe")

if audio_value:
  transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file = audio_value
  )

  transcript_text = transcript.text
  st.write(transcript_text)