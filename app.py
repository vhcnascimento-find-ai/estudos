import streamlit as st
import whisper
import os

st.title('Reprodução e Transcrição de Áudio .wav')

# Carrega o modelo Whisper
model = whisper.load_model("small")  # Você pode escolher outros modelos como 'small', 'medium', 'large'

# Adiciona um botão para upload de um único arquivo de áudio .wav
audio_file_wav = st.file_uploader("Anexe um arquivo de áudio .wav", type=["wav"])

if audio_file_wav:
    st.write(f"Arquivo enviado: {audio_file_wav.name}")
    st.audio(audio_file_wav, format='audio/wav')
    
    # Salva o arquivo de áudio enviado
    with open("uploaded_audio.wav", "wb") as f:
        f.write(audio_file_wav.getbuffer())
    
    # Transcreve o áudio usando o modelo Whisper
    result = model.transcribe("uploaded_audio.wav")
    texto_transcrito = result["text"]
    
    # Exibe o texto transcrito na tela
    st.text_area("Texto Transcrito", texto_transcrito, height=350)