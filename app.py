import streamlit as st
import soundfile as sf
import wave
import tempfile

st.title("Conversor de Áudio: OGG para WAV")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo .ogg", type=["ogg"])

if uploaded_file is not None:
    st.write("Arquivo carregado com sucesso!")
    
    # Criar um arquivo temporário para armazenar o .ogg
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_ogg:
        temp_ogg.write(uploaded_file.read())
        temp_ogg_path = temp_ogg.name
    
    # Criar um arquivo temporário para armazenar o .wav
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav_path = temp_wav.name
    
    try:
        # Ler o arquivo OGG e converter para WAV
        data, samplerate = sf.read(temp_ogg_path)
        sf.write(temp_wav_path, data, samplerate, format='WAV')
        
        st.success("Conversão concluída!")
        st.audio(temp_wav_path, format="audio/wav")
        
        with open(temp_wav_path, "rb") as f:
            st.download_button("Baixar arquivo WAV", f, file_name="convertido.wav", mime="audio/wav")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")





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
