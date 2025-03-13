import streamlit as st
from pydub import AudioSegment
import os

st.title('Reprodução e Conversão de Áudio')

# Adiciona um botão para upload de um único arquivo de áudio .ogg
audio_file = st.file_uploader("Anexe um arquivo de áudio .ogg", type=["ogg"])

if audio_file:
    st.write(f"Arquivo enviado: {audio_file.name}")
    st.audio(audio_file, format='audio/ogg')
    
    # Salva o arquivo de áudio enviado
    with open("uploaded_audio.ogg", "wb") as f:
        f.write(audio_file.getbuffer())
    
    # Converte o arquivo de áudio para .wav
    sound = AudioSegment.from_file("uploaded_audio.ogg", format="ogg")
    sound.export("converted_audio.wav", format="wav")
    
    st.success("Arquivo convertido para .wav com sucesso!")
    
    # Exibe o áudio convertido
    st.audio("converted_audio.wav", format='audio/wav')
    
    # Permite que o usuário baixe o arquivo .wav convertido
    with open("converted_audio.wav", "rb") as file:
        st.download_button(
            label="Baixar áudio convertido",
            data=file,
            file_name="converted_audio.wav",
            mime="audio/wav"
        )