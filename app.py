import streamlit as st
import speech_recognition as sr
from io import BytesIO

# Inicializa o reconhecedor
recognizer = sr.Recognizer()

st.title("Transcrição de Áudio")

# Carrega o arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["wav", "mp3"])

if uploaded_file is not None:
    # Converte o arquivo carregado para um formato que o SpeechRecognition pode usar
    audio_data = BytesIO(uploaded_file.read())
    audio_file = sr.AudioFile(audio_data)

    with audio_file as source:
        audio = recognizer.record(source)

    # Transcreve o áudio
    try:
        text = recognizer.recognize_google(audio)
        st.write("Transcrição: ", text)
    except sr.UnknownValueError:
        st.write("Google Speech Recognition não conseguiu entender o áudio")
    except sr.RequestError as e:
        st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")