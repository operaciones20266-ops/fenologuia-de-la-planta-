import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Registro de Planta", layout="wide")

# Conectar con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar datos guardados desde la nube (Google Sheets)
df_datos = conn.read(ttl=0) # ttl=0 para actualizar al instante

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
        
        # Unir el nuevo registro y guardarlo automáticamente en la nube
        df_actualizado = pd.concat([df_datos, nuevo_registro], ignore_index=True)
        conn.update(data=df_actualizado)
        
        st.success("¡Datos guardados en la nube!")
        st.rerun()
