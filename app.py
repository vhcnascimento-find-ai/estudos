import streamlit as st
import soundfile as sf
import os

st.title('Conversor de áudio .ogg para .wav')

# Adiciona um botão para upload de um único arquivo de áudio .ogg
audio_file = st.file_uploader("Anexe um arquivo de áudio .ogg", type=["ogg"])

if audio_file:
    st.write(f"Arquivo enviado: {audio_file.name}")
    st.audio(audio_file, format='audio/ogg')
    
    # Salva o arquivo de áudio enviado
    with open("uploaded_audio.ogg", "wb") as f:
        f.write(audio_file.getbuffer())
    
    # Converte o arquivo de áudio para .wav usando soundfile
    input_audio = "uploaded_audio.ogg"
    output_audio = "converted_audio.wav"
    
    # Lê o arquivo .ogg e escreve como .wav
    data, samplerate = sf.read(input_audio)
    sf.write(output_audio, data, samplerate)
    
    st.success("Arquivo convertido para .wav com sucesso!")
    
    # Exibe o áudio convertido
    st.audio(output_audio, format='audio/wav')
    
    # Permite que o usuário baixe o arquivo .wav convertido
    with open(output_audio, "rb") as file:
        st.download_button(
            label="Baixar áudio convertido",
            data=file,
            file_name=output_audio,
            mime="audio/wav"
        )