import streamlit as st
import whisper
from pydub import AudioSegment
from docx import Document

st.title('Transcrição de áudio')

# Carrega o modelo Whisper
model = whisper.load_model("small")  # Você pode escolher outros modelos como 'small', 'medium', 'large'

# Adiciona um botão para upload de múltiplos arquivos de áudio .ogg
audio_files = st.file_uploader("Anexe um ou mais arquivos de áudio .ogg", type=["ogg"], accept_multiple_files=True)

if audio_files:
    audio_names = [audio_file.name for audio_file in audio_files]
    st.write("Arquivos enviados:")
    st.write(audio_names)
    
    texto_transcrito = ""
    
    for audio_file in audio_files:
        st.write(f"Arquivo: {audio_file.name}")
        st.audio(audio_file, format='audio/ogg')
        
        # Converte o arquivo de áudio para .wav
        sound = AudioSegment.from_ogg(audio_file)
        sound.export("audio.wav", format="wav")
        
        # Transcreve o áudio usando o modelo Whisper
        result = model.transcribe("audio.wav")
        texto_transcrito += result["text"] + "\n"
    
    # Cria um documento .docx com a transcrição
    document = Document()
    document.add_paragraph(texto_transcrito)
    
    # Salva o documento .docx
    docx_filename = "transcricao.docx"
    document.save(docx_filename)
    
    # Permite que o usuário baixe o arquivo .docx
    with open(docx_filename, "rb") as file:
        btn = st.download_button(
            label="Baixar Transcrição",
            data=file,
            file_name=docx_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

