import streamlit as st
import speech_recognition as sr
from io import BytesIO

# Inicializa o reconhecedor
recognizer = sr.Recognizer()

st.title("Transcrição de Áudio")

# Carrega o arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["wav", "mp3"])

if uploaded_file is not None:
    # Reproduzir o áudio carregado
    st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[-1]}")
    
    if st.button("Iniciar Transcrição"):
        # Converte o arquivo carregado para um formato que o SpeechRecognition pode usar
        audio_data = BytesIO(uploaded_file.read())
        audio_file = sr.AudioFile(audio_data)

        with audio_file as source:
            # Ajusta o nível de ruído por mais tempo para melhorar a precisão
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.record(source)

        # Transcreve o áudio com melhores configurações
        try:
            text = recognizer.recognize_google(audio, language="pt-BR")
            st.write("Transcrição: ", text)
        except sr.UnknownValueError:
            st.write("Google Speech Recognition não conseguiu entender o áudio")
        except sr.RequestError as e:
            st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
