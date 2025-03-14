import streamlit as st
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import tempfile

# Inicializa o reconhecedor
recognizer = sr.Recognizer()

st.title("Transcrição de Áudio")

# Carrega o arquivo de áudio
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["wav", "mp3", "ogg"])

if uploaded_file is not None:
    # Converte o arquivo para WAV se for OGG
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
        if uploaded_file.name.endswith(".ogg"):
            audio_data = BytesIO(uploaded_file.read())
            audio = AudioSegment.from_file(audio_data, format="ogg")
            audio.export(temp_wav_file.name, format="wav")
            audio_path = temp_wav_file.name
        else:
            audio_path = uploaded_file

    # Reproduzir o áudio convertido
    st.audio(audio_path, format="audio/wav")
    
    if st.button("Iniciar Transcrição"):
        # Converte o arquivo carregado para um formato que o SpeechRecognition pode usar
        audio_file = sr.AudioFile(audio_path)

        with audio_file as source:
            # Ajusta o nível de ruído por mais tempo para melhorar a precisão
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
            audio = recognizer.record(source)

        # Transcreve o áudio com melhores configurações
        try:
            text = recognizer.recognize_google(audio, language="pt-BR")
            st.write("Transcrição: ", text)
        except sr.UnknownValueError:
            st.write("Google Speech Recognition não conseguiu entender o áudio")
        except sr.RequestError as e:
            st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
