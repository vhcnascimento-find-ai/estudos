import streamlit as st
import speech_recognition as sr
import os

st.title('Reprodução e Transcrição de Áudio .wav')

# Adiciona um botão para upload de um único arquivo de áudio .wav
audio_file_wav = st.file_uploader("Anexe um arquivo de áudio .wav", type=["wav"])

if audio_file_wav:
    st.write(f"Arquivo enviado: {audio_file_wav.name}")
    st.audio(audio_file_wav, format='audio/wav')
    
    # Salva o arquivo de áudio enviado
    with open("uploaded_audio.wav", "wb") as f:
        f.write(audio_file_wav.getbuffer())
    
    # Transcreve o áudio usando a biblioteca SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile("uploaded_audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            texto_transcrito = recognizer.recognize_google(audio_data, language="pt-BR")
        except sr.UnknownValueError:
            texto_transcrito = "Não foi possível transcrever o áudio."
        except sr.RequestError as e:
            texto_transcrito = f"Erro na solicitação ao serviço de reconhecimento de fala: {e}"
    
    # Exibe o texto transcrito na tela
    st.text_area("Texto Transcrito", texto_transcrito, height=300)