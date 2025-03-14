import streamlit as st
import speech_recognition as sr
from io import BytesIO
import whisper

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
        # Ajusta o nível de ruído
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    # Transcreve o áudio usando Google Speech Recognition
    try:
        text_google = recognizer.recognize_google(audio)
        st.write("Transcrição (Google Speech Recognition): ", text_google)
    except sr.UnknownValueError:
        st.write("Google Speech Recognition não conseguiu entender o áudio")
    except sr.RequestError as e:
        st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")

    # Salva o áudio em um arquivo temporário para usar com Whisper
#    with open("temp_audio.wav", "wb") as f:
#        f.write(audio_data.getbuffer())

    # Transcreve o áudio usando Whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio)
    st.write("Transcrição (Whisper): ", result["text"])