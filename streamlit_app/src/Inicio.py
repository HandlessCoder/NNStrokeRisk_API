import streamlit as st
from PIL import Image
import base64
import io  

# Inicializa el estado de la página en "Inicio" si no está definido
if "page" not in st.session_state:
    st.session_state["page"] = "Inicio"

def main():
    # Verifica en qué página está el usuario y redirige si es necesario
    if st.session_state["page"] == "Inicio":
        mostrar_inicio()
    elif st.session_state["page"] == "Stroke":
        st.switch_page("pages/Stroke.py")  

def mostrar_inicio():
    # Estilos generales de la interfaz, incluyendo colores y comportamiento del scroll
    st.markdown(
        """
        <style>
            body {
                background-color: #F4F5F9; /* Fondo gris claro */
                overflow-y: auto !important;
            }
            .stApp {
                background-color: #F4F5F9; /* Fondo gris claro */
                overflow-y: auto !important;
            }
            h1, h2, h3, h4, h5, h6, p, label {
                color: black; /* Texto en negro */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Cargar el logo desde un archivo
    logo_path = "Logo.png"
    logo = Image.open(logo_path)

    # Redimensionar el logo a un cuarto de su tamaño original
    new_size = (logo.width // 4, logo.height // 4)
    logo = logo.resize(new_size)

    # Convertir la imagen a base64 para mostrarla en HTML
    buffered = io.BytesIO()
    logo.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Mostrar el logo centrado en la interfaz
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <img src="data:image/png;base64,{logo_base64}" style="max-width: 50%; height: auto; margin-bottom: 20px; border-radius: 20px;">
        </div>
        """, unsafe_allow_html=True
    )

    # Título y descripción centrados en la pantalla
    st.markdown("""
        <h1 style='text-align: center;color: black;'>Bienvenido al Evaluador de Riesgo de Accidente Cerebrovascular</h1>
        <h3 style='text-align: center;color: black; font-size: 20px;'>Esta herramienta ayuda a evaluar el riesgo de accidente cerebrovascular basado en diversos factores de salud.</h3>
    """, unsafe_allow_html=True)

    # Estilos para el botón de evaluación
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #A2E4B8; /* Verde claro */
            color: black; /* Texto negro */
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 30px;
            border: none;
            display: block;
            margin: 20px auto;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        .stButton>button:hover {
            background-color: #8DCFA0; /* Verde más oscuro */
            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    # Botón para navegar a la evaluación
    if st.button("Hacer Evaluación"):
        st.switch_page("pages/Stroke.py")  

if __name__ == "__main__":
    main()
