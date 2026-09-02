import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import gspread

# Configuración de página
st.set_page_config(page_title="Registro de Planta", layout="wide")

# Conexión directa con Google Sheets usando Secrets
@st.cache_resource
def get_gsheet():
    creds = dict(st.secrets["gdrive"])
    # Reparar saltos de línea de la private key
    creds["private_key"] = creds["private_key"].replace("\\n", "\n")
    gc = gspread.service_account_from_dict(creds)
    sheet_url = st.secrets["spreadsheet_url"]
    return gc.open_by_url(sheet_url).sheet1

sheet = get_gsheet()

# Cargar datos desde la nube
try:
    records = sheet.get_all_records()
    df_datos = pd.DataFrame(records)
except Exception:
    df_datos = pd.DataFrame(columns=["nudo", "longitud_cm", "grosor_mm"])

nudos = df_datos.to_dict(orient="records") if not df_datos.empty else []

st.title("🌱 PLANTA DE ESTUDIO (POLEPOS)")

columna1, columna2 = st.columns([1, 2])

with columna1:
    st.subheader("Registro de Crecimiento")
    longitud = st.number_input("Longitud del entrenudo (cm):", min_value=0.0, step=0.1)
    grosor = st.number_input("Grosor del tallo (mm):", min_value=0.0, step=0.1)

    if st.button("+ Agregar a la Planta"):
        nuevo_nudo = len(nudos) + 1
        # Insertar nueva fila en Google Sheets
        sheet.append_row([nuevo_nudo, longitud, grosor])
        st.success("¡Datos guardados!")
        st.rerun()

with columna2:
    st.subheader("Visualización del Tallo")
    if nudos:
        fig, ax = plt.subplots(figsize=(4, 6))
        
        y_pos = 0
        for i, nudo in enumerate(nudos):
            h = float(nudo.get("longitud_cm", 1.0))
            w = float(nudo.get("grosor_mm", 1.0)) / 10.0
            
            rect = patches.Rectangle((-w / 2, y_pos), w, h, linewidth=1, edgecolor='darkgreen', facecolor='lightgreen')
            ax.add_patch(rect)
            ax.text(w / 2 + 0.2, y_pos + (h / 2), f"Nudo {i+1}\nL: {h}cm | G: {nudo.get('grosor_mm', 0)}mm", verticalalignment='center')
            y_pos += h

        ax.set_xlim(-2, 5)
        ax.set_ylim(0, max(y_pos + 2, 5))
        ax.set_aspect('equal')
        ax.axis('off')
        
        st.pyplot(fig)
    else:
        st.info("No hay nudos registrados aún. Agrega el primero usando el formulario.")
