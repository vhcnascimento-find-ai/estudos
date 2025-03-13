import streamlit as st
import whisper
import soundfile as sf
import os

st.title('Conversor de áudio .ogg para .wav e Transcrição de Áudio')

# Seção para conversão de .ogg para .wav
st.header('Conversão de .ogg para .wav')

# Adiciona um botão para upload de um único arquivo de áudio .ogg
audio_file_ogg = st.file_uploader("Anexe um arquivo de áudio .ogg", type=["ogg"])

if audio_file_ogg:
    st.write(f"Arquivo enviado: {audio_file_ogg.name}")
    st.audio(audio_file_ogg, format='audio/ogg')
    
    # Salva o arquivo de áudio enviado
    with open("uploaded_audio.ogg", "wb") as f:
        f.write(audio_file_ogg.getbuffer())
    
    # Converte o arquivo de áudio para .wav usando soundfile
    input_audio = "uploaded_audio.ogg"
    output_audio = "converted_audio.wav"
    
    # Lê o arquivo .ogg e escreve como .wav
    data, samplerate = sf.read(input_audio)
    sf.write(output_audio, data, samplerate)
    
    st.success("Arquivo convertido para .wav com sucesso!")
    
    # Permite que o usuário baixe o arquivo .wav convertido
    with open(output_audio, "rb") as file:
        st.download_button(
            label="Baixar áudio convertido",
            data=file,
            file_name=output_audio,
            mime="audio/wav"
        )

# Seção para transcrição de áudio .wav
st.header('Transcrição de Áudio .wav')

# Carrega o modelo Whisper
model = whisper.load_model("small")  # Você pode escolher outros modelos como 'small', 'medium', 'large'

# Adiciona um botão para upload de um único arquivo de áudio .wav
audio_file_wav = st.file_uploader("Anexe um arquivo de áudio .wav", type=["wav"])

if audio_file_wav:
    st.write(f"Arquivo enviado: {audio_file_wav.name}")
    st.audio(audio_file_wav, format='audio/wav')
    
    # Salva o arquivo de áudio enviado
    with open("uploaded_audio.wav", "wb") as f:
        f.write(audio_file_wav.getbuffer())
    
    # Transcreve o áudio usando o modelo Whisper
    result = model.transcribe("uploaded_audio.wav")
    texto_transcrito = result["text"]
    
    # Exibe o texto transcrito na tela
    st.text_area("Texto Transcrito", texto_transcrito, height=350)