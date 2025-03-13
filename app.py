import streamlit as st

st.title('Reprodução de Áudio .wav')

# Adiciona um botão para upload de um único arquivo de áudio .wav
audio_file_wav = st.file_uploader("Anexe um arquivo de áudio .wav", type=["wav"])

if audio_file_wav:
    st.write(f"Arquivo enviado: {audio_file_wav.name}")
    st.audio(audio_file_wav, format='audio/wav')