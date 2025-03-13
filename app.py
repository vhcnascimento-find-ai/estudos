import streamlit as st

st.title('Transcrição de áudio')

# Adiciona um botão para upload de múltiplos arquivos de áudio .ogg
audio_files = st.file_uploader("Anexe um ou mais arquivos de áudio .ogg", type=["ogg"], accept_multiple_files=True)

if audio_files:
    audio_names = [audio_file.name for audio_file in audio_files]
    st.write("Arquivos enviados:")
    st.write(audio_names)
    
    for audio_file in audio_files:
        st.write(f"Arquivo: {audio_file.name}")
        st.audio(audio_file, format='audio/ogg')