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

st.title('Reprodução de Áudio')

# Adiciona um botão para upload de um único arquivo de áudio .ogg
audio_file = st.file_uploader("Anexe um arquivo de áudio .ogg", type=["ogg"])

if audio_file:
    st.write(f"Arquivo enviado: {audio_file.name}")
    st.audio(audio_file, format='audio/ogg')