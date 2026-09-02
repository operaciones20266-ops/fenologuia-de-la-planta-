import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Registro de Planta", layout="wide")

# Conestar con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar datos guardados desde la nube (Google Sheets)
df_datos = conn.read(ttl=0)  # ttl=0 para actualizar al instante

# Convertir la hoja a lista de nudos para tu código actual
nudos = df_datos.to_dict(orient="records") if not df_datos.empty else []

st.title("🌱 PLANTA DE ESTUDIO (POLEPOS)")

columna1, columna2 = st.columns([1, 2])

with columna1:
    st.subheader("Registro de Crecimiento")
    longitud = st.number_input("Longitud del entrenudo (cm):", min_value=0.0, step=0.1)
    grosor = st.number_input("Grosor del tallo (mm):", min_value=0.0, step=0.1)

    if st.button("+ Agregar a la Planta"):
        nuevo_registro = pd.DataFrame([{
            "nudo": len(nudos) + 1,
            "longitud_cm": longitud,
            "grosor_mm": grosor
        }])
        
        # Guardar en Google Sheets
        df_actualizado = pd.concat([df_datos, nuevo_registro], ignore_index=True)
        conn.update(data=df_actualizado)
        st.success("¡Datos guardados!")
        st.rerun()

with columna2:
    st.subheader("Visualización del Tallo")
    if nudos:
        fig, ax = plt.subplots(figsize=(4, 6))
        
        # Dibujar cada nudo guardado
        y_pos = 0
        for i, nudo in enumerate(nudos):
            h = nudo.get("longitud_cm", 1.0)
            w = nudo.get("grosor_mm", 1.0) / 10.0  # convertir mm a cm para la escala
            
            # Dibujar el entrenudo como un rectángulo
            rect = patches.Rectangle((-w / 2, y_pos), w, h, linewidth=1, edgecolor='darkgreen', facecolor='lightgreen')
            ax.add_patch(rect)
            
            # Etiqueta del nudo
            ax.text(w / 2 + 0.2, y_pos + (h / 2), f"Nudo {i+1}\nL: {h}cm | G: {nudo.get('grosor_mm', 0)}mm", verticalalignment='center')
            
            y_pos += h

        ax.set_xlim(-2, 5)
        ax.set_ylim(0, max(y_pos + 2, 5))
        ax.set_aspect('equal')
        ax.axis('off')
        
        st.pyplot(fig)
    else:
        st.info("No hay nudos registrados aún. Agrega el primero usando el formulario de la izquierda.")
