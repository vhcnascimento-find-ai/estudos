import streamlit as st
import whisper
from pydub import AudioSegment
import imageio_ffmpeg as ffmpeg

# Configura o pydub para usar o ffmpeg do imageio-ffmpeg
AudioSegment.converter = ffmpeg.get_ffmpeg_exe()

st.title('Transcrição de áudio')

# Carrega o modelo Whisper
model = whisper.load_model("small")  # Você pode escolher outros modelos como 'small', 'medium', 'large'

# Adiciona um botão para upload de um único arquivo de áudio .ogg
audio_file = st.file_uploader("Anexe um arquivo de áudio .ogg", type=["ogg"])

if audio_file:
    st.write(f"Arquivo enviado: {audio_file.name}")
    st.audio(audio_file, format='audio/ogg')
    
    # Converte o arquivo de áudio para .wav
    sound = AudioSegment.from_ogg(audio_file)
    sound.export("audio.wav", format="wav")
    
    # Transcreve o áudio usando o modelo Whisper
    result = model.transcribe("audio.wav")
    texto_transcrito = result["text"]
    
    # Exibe o texto transcrito na tela
    st.text_area("Texto Transcrito", texto_transcrito, height=300)