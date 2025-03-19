import streamlit as st
import soundfile as sf
import tempfile
import speech_recognition as sr
import time
from docx import Document

st.title("Conversor e Transcritor de Áudio: OGG para WAV")

# 📌 Função para dividir o áudio em segmentos menores
def divide_audio(file_path, segment_length=60):
    data, samplerate = sf.read(file_path)
    total_length = len(data) / samplerate
    segments = []
    for start in range(0, int(total_length), segment_length):
        end = start + segment_length
        segment = data[start * samplerate:end * samplerate]
        segments.append(segment)
    return segments, samplerate

# 📌 Função para transcrever um segmento de áudio
def transcrever_segmento(segment, samplerate, recognizer, segment_number):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_segment:
            sf.write(temp_segment.name, segment, samplerate, format='WAV')
            with sr.AudioFile(temp_segment.name) as source:
                audio = recognizer.record(source)
                return recognizer.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return f"[Segmento {segment_number}] Google Speech Recognition não conseguiu entender o áudio."
    except sr.RequestError as e:
        return f"[Segmento {segment_number}] Erro ao solicitar reconhecimento de fala: {e}"

# 📌 Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo .ogg", type=["ogg"])

if uploaded_file is not None:
    st.write("📂 Arquivo carregado com sucesso!")

    # Criar arquivos temporários
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_ogg:
        temp_ogg.write(uploaded_file.read())
        temp_ogg_path = temp_ogg.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        # 📌 Converter de OGG para WAV
        data, samplerate = sf.read(temp_ogg_path)
        sf.write(temp_wav_path, data, samplerate, format='WAV')

        st.success("🎵 Conversão concluída!")
        st.audio(temp_wav_path, format="audio/wav")
        st.write("⌛ *A transcrição pode levar um tempo equivalente à duração do áudio. Por favor, aguarde!*")

        if st.button("▶️ Iniciar Transcrição"):
            # 📌 Inicializa o reconhecedor
            recognizer = sr.Recognizer()
            
            # 📌 Divide o áudio em segmentos
            segments, samplerate = divide_audio(temp_wav_path)
            total_segments = len(segments)
            transcription = ""

            st.write(f"🔹 O áudio foi dividido em {total_segments} segmento(s)")

            start_time = time.time()  # Marca o tempo de início
            progress_bar = st.progress(0)  # Barra de progresso
            progress_text = st.empty()  # Espaço para atualizar o progresso

            # 📌 Loop de transcrição com progresso
            for i, segment in enumerate(segments):
                text = transcrever_segmento(segment, samplerate, recognizer, i + 1)
                transcription += text + " "

                # Atualiza a barra de progresso e o texto
                progress = (i + 1) / total_segments
                progress_bar.progress(progress)
                progress_text.text(f"🔄 Progresso: {int(progress * 100)}% concluído")

                time.sleep(0.1)  # Pequeno delay para atualização fluida da interface
            
            end_time = time.time()  # Marca o tempo de fim
            elapsed_time = end_time - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)

            st.success(f"✅ Transcrição concluída em {minutes} min e {seconds} seg!")
            st.session_state.transcription = transcription
            st.text_area("📄 Texto Transcrito:", transcription, height=200)
            
    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")

# 📌 Exportação para Word se houver transcrição
if "transcription" in st.session_state:
    file_name = st.text_input("✏️ Nome do arquivo Word (sem extensão):", "Transcrição")
    st.markdown('<p style="color:red;">⚠️ Aperte enter para confirmar o nome do arquivo antes de exportar.</p>', unsafe_allow_html=True)
    doc = Document()
    doc.add_paragraph(st.session_state.transcription)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        doc.save(temp_docx.name)
        temp_docx_path = temp_docx.name

    with open(temp_docx_path, "rb") as f:
        st.download_button("💾 Exportar Transcrição para Word", f, file_name=f"{file_name}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
