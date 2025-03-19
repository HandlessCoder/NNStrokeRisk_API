import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configurar la API Key desde una variable de entorno
api_key = "AIzaSyC-CnTocy4rY5wqj944xyNGFK8MbzBFE_4"


# Configuración de la clave API de Generative AI de Google para realizar solicitudes
api_key = "AIzaSyC-CnTocy4rY5wqj944xyNGFK8MbzBFE_4"

# Verifica si la clave API está configurada correctamente; muestra un error en caso contrario
if not api_key:
    st.error("No se encontró la clave API. Asegúrate de configurarla correctamente.")
else:
    genai.configure(api_key=api_key)

def obtener_recomendaciones(datos_paciente):
    """
    Genera recomendaciones de salud basadas en los datos proporcionados por el paciente.

    Args:
        datos_paciente (str): Información del paciente, como edad, género y síntomas.

    Returns:
        str: Texto con recomendaciones generadas por el modelo o un mensaje de error.
    """
    try:
        # Selecciona el modelo de IA de Google para generar contenido basado en los datos proporcionados
        model = genai.GenerativeModel("gemini-1.5-flash")  
        response = model.generate_content(f"Basado en estos datos del paciente: {datos_paciente}, "
                                          "proporciona recomendaciones para mejorar su salud.")
        return response.text if response else "No se pudo generar una respuesta."
    except Exception as e:
        # Devuelve un mensaje de error en caso de que falle la API
        return f"Error en la API: {str(e)}"
    

def main():

    # Estilo personalizado para cambiar colores, tipografías y elementos de la interfaz
    st.markdown(
    """
    <style>
        body {
            background-color: #F4FAF0;  /* Azul claro */
        }
        .stApp {
            background-color: #F4FAF0;  /* Azul claro */
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: black; /* Asegura que todos los textos sean negros */
        }
        /* Estilo para el ícono del tooltip (signo de interrogación) */
        .stTooltipIcon svg {
            fill: gray !important; /* Cambia el color del ícono a gris */
        }
        /* Estilo para el contenido del tooltip */
        .stTooltipContent {
            background-color: white !important; /* Fondo blanco */
            color: gray !important; /* Letra gris */
            border: 1px solid #ccc !important; /* Borde gris claro */
            border-radius: 5px !important; /* Bordes redondeados */
            padding: 10px !important; /* Espaciado interno */
        }
        /* Estilo para el campo de edad */
        .stNumberInput input {
            background-color: white !important; /* Fondo blanco */
            color: black !important; /* Letra negra */
        }
        /* Estilo para los botones de incremento y decremento en el campo de edad */
        .stNumberInput button {
            background-color: #A2E4B8 !important; /* Fondo verde */
            color: white !important; /* Letra blanca */
            border: 1px solid #A2E4B8 !important; /* Borde verde */
        }
        .stNumberInput button:hover {
            background-color: #64AC8F !important; /* Fondo verde oscuro al pasar el cursor */
            border-color: #64AC8F !important; /* Borde verde oscuro al pasar el cursor */
        }
        /* Estilo para los checkboxes */
        .stCheckbox label {
            color: white !important; /* Letra negra */
        }
        .stCheckbox .stCheckboxBox {
            background-color: white !important; /* Fondo blanco */
            border-color: white !important; /* Borde negro */
        }
        /* Estilo para el cuadrito interior del checkbox */
        .stCheckbox input[type="checkbox"] {
            background-color: white !important; /* Fondo blanco */
            border-color: white !important; /* Borde negro */
        }
        /* Estilo para los botones */
        .stButton button {
            background-color: #A2E4B8 !important; /* Fondo verde */
            color: white !important; /* Letra blanca */
            border-radius: 5px !important; /* Bordes redondeados */
            border: 1px solid #A2E4B8 !important; /* Borde verde */
            padding: 10px 20px !important; /* Espaciado interno */
        }
        .stButton button:hover {
            background-color: #64AC8F !important; /* Fondo verde oscuro al pasar el cursor */
            border-color: #64AC8F !important; /* Borde verde oscuro al pasar el cursor */
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # Mostrar título y descripción centrados
    st.markdown("""
        <h1 style='text-align: center;color: black;'>Evaluación de Riesgo de Accidente Cerebrovascular</h1>
        <h3 style='text-align: center;color: black; font-size: 20px;'>Por favor complete la encuesta.</h3>
    """, unsafe_allow_html=True)
    
    # Entrada numérica con descripción
    age = st.number_input("Edad del paciente", min_value=0, max_value=120, step=1, help="Ingrese la edad del paciente en años.")
    
    # Selección de género con descripción
    gender = st.radio("Género", ("Masculino", "Femenino"), help="Seleccione el género del paciente.")
    
    # Variables binarias con checkboxes y descripciones
    symptoms = {
        "chest_pain": ("Dolor en el pecho", "Sensación de opresión, presión o ardor en el pecho."),
        "high_blood_pressure": ("Hipertensión arterial", "Presión arterial elevada que puede aumentar el riesgo de un accidente cerebrovascular."),
        "irregular_heartbeat": ("Latidos irregulares", "Sensación de palpitaciones o latidos irregulares en el corazón."),
        "shortness_of_breath": ("Falta de aire", "Dificultad para respirar o sensación de ahogo."),
        "fatigue_weakness": ("Fatiga o debilidad", "Sensación de agotamiento o falta de energía."),
        "dizziness": ("Mareo", "Sensación de inestabilidad o pérdida de equilibrio."),
        "swelling_edema": ("Hinchazón o edema", "Acumulación de líquidos en piernas, tobillos o pies."),
        "neck_jaw_pain": ("Dolor en el cuello o mandíbula", "Malestar en estas zonas que puede estar relacionado con problemas cardiovasculares."),
        "excessive_sweating": ("Sudoración excesiva", "Transpiración abundante sin causa aparente."),
        "persistent_cough": ("Tos persistente", "Tos que no desaparece y puede estar relacionada con problemas cardiovasculares."),
        "nausea_vomiting": ("Náuseas o vómitos", "Sensación de malestar estomacal o ganas de vomitar."),
        "chest_discomfort": ("Malestar en el pecho", "Sensación de incomodidad o presión en el área del pecho."),
        "cold_hands_feet": ("Manos o pies fríos", "Extremidades frías debido a problemas circulatorios."),
        "snoring_sleep_apnea": ("Ronquidos o apnea del sueño", "Interrupciones en la respiración durante el sueño."),
        "anxiety_doom": ("Sensación de ansiedad o presentimiento de fatalidad", "Sensación repentina de angustia sin causa aparente.")
    }
    
    # Creación de checkboxes con descripciones
    symptoms_selected = {}
    for key, (label, description) in symptoms.items():
        symptoms_selected[key] = st.checkbox(label, help=description)
        
    # Centrar el botón con CSS en Streamlit
    st.markdown(
        """
        <style>
            .stButton > button {
                display: block;
                margin: 0 auto;
                background-color: #A2E4B8 !important; /* Color verde */
                color: white !important; /* Texto en blanco */
                font-size: 16px !important;
                border-radius: 5px !important;
                padding: 10px 20px !important;
                border: none !important;
                cursor: pointer !important;
            }
            .stButton > button:hover {
                background-color: #64AC8F !important; /* Verde oscuro al pasar el cursor */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Botón centrado
    if st.button("Predecir Riesgo"):
        patient_data = {
            "age": age,
            "gender": gender,
            **symptoms_selected
        }
        
        # Título centrado en negro
        st.markdown(
            """
            <h1 style='text-align: center; color: black;'>🩺 Recomendaciones de Salud por Gemini AI</h1>
            """,
            unsafe_allow_html=True
        )

        symptoms_list = [label for label, selected in symptoms_selected.items() if selected]
        symptoms_text = ", ".join(symptoms_list) if symptoms_list else "Sin síntomas reportados"

        datos_paciente = f"Edad: {age} años\nGénero: {gender}\nSíntomas reportados: {symptoms_text}"

        recomendaciones = obtener_recomendaciones(datos_paciente)
        
        #  Limpieza y formato del texto generado por la IA
        recomendaciones = recomendaciones.replace("**", "")  # Elimina negritas en Markdown
        recomendaciones = recomendaciones.replace("\n\n", "\n")  # Elimina dobles saltos de línea

        #  Separar en líneas y limpiar
        recomendaciones_lista = recomendaciones.split("\n")
        recomendaciones_lista = [item.strip() for item in recomendaciones_lista if item.strip()]  # Elimina líneas vacías

        #  Convertir listas correctamente
        recomendaciones_formateadas = []
        for item in recomendaciones_lista:
            if item.startswith("* "):  
                item = item.replace("* ", "", 1)  # Elimina solo el primer *
                recomendaciones_formateadas.append(f"<li>{item}</li>")
            else:
                recomendaciones_formateadas.append(f"<p>{item}</p>")  # Mantiene los párrafos sin viñetas

        # Unir todo asegurando que las listas sean válidas en HTML
        recomendaciones_html = "".join(recomendaciones_formateadas)

        # Aplicar formato con HTML y CSS
        st.subheader("🔎 Recomendaciones:")
        st.markdown(
            f"""
            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 5px solid #4CAF50;'>
                <p style='color: black; font-size: 18px; font-weight: bold;'>Recomendaciones Generales:</p>
                <ul style="color: black; font-size: 16px; line-height: 1.6;">
                    {recomendaciones_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )



        
if __name__ == "__main__":
    main()



