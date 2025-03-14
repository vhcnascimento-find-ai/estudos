import streamlit as st
import os
import whisper
from pydub import AudioSegment
from docx import Document

def transcrever_audio(audio_file_path):
    try:
        model = whisper.load_model("small")
        sound = AudioSegment.from_file(audio_file_path)
        temp_wav_path = "temp_audio.wav"
        sound.export(temp_wav_path, format="wav")
        result = model.transcribe(temp_wav_path)
        os.remove(temp_wav_path)
        return result["text"]
    except FileNotFoundError as e:
        st.error(f"Erro: Arquivo não encontrado - {e}")
        return ""
    except Exception as e:
        st.error(f"Erro ao processar áudio: {e}")
        return ""

st.title("Transcrição de Áudio com Whisper")

uploaded_files = st.file_uploader("Envie arquivos de áudio", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

if uploaded_files:
    texto_transcrito = ""
    for uploaded_file in uploaded_files:
        st.write(f"Transcrevendo: {uploaded_file.name}")
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        texto = transcrever_audio(temp_file_path)
        texto_transcrito += texto + "\n"
        os.remove(temp_file_path)
    
    if texto_transcrito.strip():
        st.text_area("Texto Transcrito", texto_transcrito, height=300)
        
        doc = Document()
        doc.add_paragraph(texto_transcrito)
        doc_path = "transcricao.docx"
        doc.save(doc_path)
        
        with open(doc_path, "rb") as f:
            st.download_button("Baixar Transcrição", f, file_name="transcricao.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    else:
        st.warning("Nenhum texto foi transcrito. Verifique os arquivos de áudio e tente novamente.")
