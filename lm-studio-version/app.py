# app.py
import streamlit as st
import requests

# Configuración inicial
st.set_page_config(page_title="Chat con LM Studio", page_icon="🤖")
st.title("🧠 Chatbot con DeepSeek-R1-Distill-Qwen-7B")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración del Modelo")
    
    # Configuración específica de LM Studio
    st.subheader("Configuración LM Studio")
    api_base = st.text_input(
        "Endpoint de la API",
        value="http://localhost:1234/v1",  # Puerto default de LM Studio
        help="URL base de la API local de LM Studio"
    )
    model_name = st.text_input(
        "Nombre del Modelo",
        value="lmstudio-community/DeepSeek-R1-Distill-Qwen-7B-GGUF",
        disabled=True
    )
    
    # Parámetros del modelo
    temperature = st.slider("Creatividad (temperature)", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Máximo de tokens", 100, 2000, 500)

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Función para generar respuestas
def generate_response(user_input):
    try:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": user_input}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = requests.post(
            f"{api_base}/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            st.error(f"Error en la API: {response.text}")
            return ""
            
        return response.json()["choices"][0]["message"]["content"]
        
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return ""

# Entrada de usuario
if prompt := st.chat_input("Hazme una pregunta..."):
    # Agregar mensaje de usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_response(prompt)
            
        # Mostrar y guardar respuesta
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Sección de feedback
st.sidebar.markdown("---")
st.sidebar.markdown("### Feedback")
if st.sidebar.button("👍 Respuesta útil"):
    st.sidebar.success("¡Gracias por tu feedback!")
if st.sidebar.button("👎 Respuesta incorrecta"):
    st.sidebar.warning("¡Gracias por tu feedback!")

# Instrucciones para ejecutar
# Para usar: 
# 1. Instalar dependencias: pip install streamlit requests
# 2. Ejecutar: streamlit run app.py