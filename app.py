import streamlit as st
import os
import whisper
from pydub import AudioSegment
from docx import Document

def transcrever_audio(audio_file):
    model = whisper.load_model("small")
    sound = AudioSegment.from_file(audio_file)
    sound.export("audio.wav", format="wav")
    result = model.transcribe("audio.wav")
    return result["text"]

st.title("Transcrição de Áudio com Whisper")

uploaded_files = st.file_uploader("Envie arquivos de áudio", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

if uploaded_files:
    texto_transcrito = ""
    for audio_file in uploaded_files:
        st.write(f"Transcrevendo: {audio_file.name}")
        texto = transcrever_audio(audio_file)
        texto_transcrito += texto + "\n"
    
    st.text_area("Texto Transcrito", texto_transcrito, height=300)
    
    doc = Document()
    doc.add_paragraph(texto_transcrito)
    doc_path = "transcricao.docx"
    doc.save(doc_path)
    
    with open(doc_path, "rb") as f:
        st.download_button("Baixar Transcrição", f, file_name="transcricao.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
