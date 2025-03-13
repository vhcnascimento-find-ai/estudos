import streamlit as st
import whisper
from pydub import AudioSegment
import imageio_ffmpeg as ffmpeg
import os

# Configura o pydub para usar o ffmpeg do imageio-ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()
AudioSegment.converter = ffmpeg_path

# Verifica se o ffmpeg está configurado corretamente
if not os.path.isfile(ffmpeg_path):
    st.error("FFmpeg não encontrado. Verifique a instalação do FFmpeg.")
else:
    st.success("FFmpeg configurado corretamente.")

st.title('Transcrição de áudio')

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
    
    # Converte o arquivo de áudio para .wav
    sound = AudioSegment.from_ogg("uploaded_audio.ogg")
    sound.export("audio.wav", format="wav")
    
    # Transcreve o áudio usando o modelo Whisper
    result = model.transcribe("audio.wav")
    texto_transcrito = result["text"]
    
    # Exibe o texto transcrito na tela
    st.text_area("Texto Transcrito", texto_transcrito, height=300)