import streamlit as st
import whisper
import soundfile as sf
import os

st.title('Reprodução e Transcrição de Áudio')

# Carrega o modelo Whisper
model = whisper.load_model("small")  # Você pode escolher outros modelos como 'small', 'medium', 'large'

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
    
    # Transcreve o áudio usando o modelo Whisper
    result = model.transcribe(output_audio)
    texto_transcrito = result["text"]
    
    # Exibe o texto transcrito na tela
    st.text_area("Texto Transcrito", texto_transcrito, height=350)