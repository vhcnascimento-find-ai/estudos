import streamlit as st
import soundfile as sf
import tempfile
import speech_recognition as sr
from io import BytesIO
from docx import Document
import time

st.title("Transcritor de Áudio: OGG para WAV")

# Função para dividir o áudio em segmentos menores
def divide_audio(file_path, segment_length=60):
    data, samplerate = sf.read(file_path)
    total_length = len(data) / samplerate
    segments = []
    for start in range(0, int(total_length), segment_length):
        end = start + segment_length
        segment = data[start * samplerate:end * samplerate]
        segments.append(segment)
    return segments, samplerate

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
        
        st.write("Conversão concluída!")
        st.audio(temp_wav_path, format="audio/wav")
        st.write("*A transcrição pode levar um tempo equivalente à duração do áudio. Por favor, aguarde!")
        
        if st.button("Iniciar Transcrição"):
            # Inicializa o reconhecedor
            recognizer = sr.Recognizer()
            
            # Divide o áudio em segmentos menores
            segments, samplerate = divide_audio(temp_wav_path)
            transcription = ""
            
            start_time = time.time()  # Início da medição do tempo
            
            for i, segment in enumerate(segments):
                st.write(f"Transcrevendo o segmento {i + 1} de {len(segments)}")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_segment:
                    sf.write(temp_segment.name, segment, samplerate, format='WAV')
                    with sr.AudioFile(temp_segment.name) as source:
                        audio = recognizer.record(source)
                        try:
                            text = recognizer.recognize_google(audio, language="pt-BR")
                            transcription += text + " "
                        except sr.UnknownValueError:
                            st.write("Google Speech Recognition não conseguiu entender o áudio")
                        except sr.RequestError as e:
                            st.write(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
            
            end_time = time.time()  # Fim da medição do tempo
            transcription_time = end_time - start_time
            transcription_minutes = transcription_time // 60
            transcription_seconds = transcription_time % 60
            st.write(f"Tempo de transcrição: {int(transcription_minutes)} minutos e {int(transcription_seconds)} segundos")
            
            st.session_state.transcription = transcription
            st.write("Transcrição: ", transcription)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

# Adiciona campo de texto para o nome do arquivo e botão para exportar a transcrição para Word se a transcrição estiver disponível
if "transcription" in st.session_state:
    file_name = st.text_input("Nome do arquivo Word (sem extensão):", "Transcrição")
    st.markdown('<p style="color:red;">⚠️ Aperte enter para confirmar o nome do arquivo antes de exportar.</p>', unsafe_allow_html=True)
    doc = Document()
    doc.add_paragraph(st.session_state.transcription)
    
    # Salva o documento temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        doc.save(temp_docx.name)
        temp_docx_path = temp_docx.name
    
    with open(temp_docx_path, "rb") as f:
        st.download_button("Exportar Transcrição para Word", f, file_name=f"{file_name}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
