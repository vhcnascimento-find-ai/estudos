import streamlit as st

st.title('Hello World')
st.write('This is a simple Streamlit app.')

# Adiciona um botão para upload de múltiplos arquivos de áudio .ogg
audio_files = st.file_uploader("Upload um ou mais arquivos de áudio .ogg", type=["ogg"], accept_multiple_files=True)

if audio_files:
    for audio_file in audio_files:
        st.audio(audio_file, format='audio/ogg')
        st.write(f"Arquivo: {audio_file.name}")