import streamlit as st
import google.generativeai as genai
import os

# Configurar clave de API
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyAOvW66WD-ff-r3S4fuIKHzHdMouehGkfU")
genai.configure(api_key=API_KEY)

# Estilos personalizados
st.markdown(
    """
    <style>
        body { background-color: #181818; color: #f5f5f5; font-family: 'Arial', sans-serif; }
        .chat-container { padding: 15px; border-radius: 10px; background: #242424; width: 85%; margin: 10px auto; }
        .msg-user { background: #1e90ff; color: white; border-radius: 10px; padding: 10px; text-align: right; }
        .msg-bot { background: #f1f1f1; color: black; border-radius: 10px; padding: 10px; text-align: left; }
        .input-container { background: white; color: black; border-radius: 6px; padding: 8px; width: 100%; }
        .send-btn { background: #1e90ff; color: white; border: none; border-radius: 6px; padding: 10px 16px; cursor: pointer; }
        .send-btn:hover { background: #0066cc; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial en session_state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

def generar_respuesta(texto):
    modelo = genai.GenerativeModel("gemini-pro")
    return modelo.generate_content(texto).text

st.title("🤖 Chat IA - Gemini")

# Mostrar historial de chat
chat_box = st.container()
with chat_box:
    for mensaje in st.session_state.chat_log:
        estilo = "msg-user" if mensaje["rol"] == "usuario" else "msg-bot"
        st.markdown(f'<div class="chat-container {estilo}">{mensaje["contenido"]}</div>', unsafe_allow_html=True)

# Entrada de usuario con formulario
with st.form(key="formulario_chat", clear_on_submit=True):
    entrada_usuario = st.text_input("", placeholder="Escribe aquí...", key="entrada_usuario")
    enviado = st.form_submit_button("Enviar")

if enviado and entrada_usuario.strip():
    st.session_state.chat_log.append({"rol": "usuario", "contenido": entrada_usuario})
    respuesta = generar_respuesta(entrada_usuario)
    st.session_state.chat_log.append({"rol": "bot", "contenido": respuesta})
    st.rerun()

# Botón para reiniciar conversación
if st.button("Nuevo Chat"):
    st.session_state.chat_log.clear()
    st.rerun()
