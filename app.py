import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

st.set_page_config(page_title="Registro de Planta", layout="wide")

# Estilo personalizado en CSS para simular el tema oscuro del Dashboard
st.markdown("""
<style>
    .main { background-color: #121e17; }
    h1, h2, h3, p, label { color: #e0f2e9 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌱 PLANTA DE ESTUDIO (FASE VEGETATIVA)")

if "nudos" not in st.session_state:
    st.session_state["nudos"] = [
    ]

col1, col2 = st.columns([1.2, 1])

with col2:
    st.subheader("📋 REGISTRO DE CRECIMIENTO")
    nombre_nudo = f"Nudo {len(st.session_state['nudos']) + 1}"
    st.info(f"Registrando: **{nombre_nudo}**")
    
    longitud = st.number_input("Longitud del entrenudo (cm):", min_value=0.5, value=4.0, step=0.5)
    grosor = st.number_input("Grosor del tallo (mm):", min_value=1.0, value=4.0, step=0.5)
    
    if st.button("➕ Agregar a la Planta", use_container_width=True):
        st.session_state["nudos"].append({
            "nudo": nombre_nudo,
            "longitud": longitud,
            "grosor": grosor
        })
        st.success(f"{nombre_nudo} agregado.")
        st.rerun()

with col1:
    # Crear gráfica con estética de ilustración técnica
    fig, ax = plt.subplots(figsize=(6, 9), facecolor='#1b2a22')
    ax.set_facecolor('#1b2a22')
    
    altura_acumulada = 0
    puntos_nudos = [(0, 0)]
    
    # Dibujar tallo con grosor variable
    for item in st.session_state["nudos"]:
        y_inicio = altura_acumulada
        y_fin = altura_acumulada + item["longitud"]
        grosor_linea = item["grosor"] * 1.5
        
        # Segmento del tallo
        ax.plot([0, 0], [y_inicio, y_fin], color='#4caf50', linewidth=grosor_linea, zorder=2, solid_capstyle='round')
        
        altura_acumulada = y_fin
        puntos_nudos.append((0, altura_acumulada))
        
        # Dibujar Hojas en cada nudo
        for lado in [-1, 1]:
            # Forma de la hoja simplificada
            verts = [
                (0, y_fin), 
                (lado * 2.5, y_fin + 1.0), 
                (lado * 3.5, y_fin + 0.2), 
                (lado * 1.5, y_fin - 0.8), 
                (0, y_fin)
            ]
            codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor='#388e3c', edgecolor='#81c784', lw=1.2, zorder=3, alpha=0.9)
            ax.add_patch(patch)
            
            # Nervadura de la hoja
            ax.plot([0, lado * 3.2], [y_fin, y_fin + 0.6], color='#a5d6a7', lw=0.8, zorder=4)

        # Punto del Nudo
        ax.plot(0, y_fin, marker='o', color='#a5d6a7', markersize=8, zorder=5)
        
        # Etiqueta tipo Cuadro de Información (Callout)
        ax.annotate(
            f"{item['nudo']}\nAlt: {y_fin} cm | Grosor: {item['grosor']} mm",
            xy=(0, y_fin), xytext=(2.5 if len(puntos_nudos) % 2 == 0 else -6.5, y_fin),
            bbox=dict(boxstyle="round,pad=0.4", fc="#263a2e", ec="#81c784", lw=1),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="#81c784", lw=1.2),
            color="#e0f2e9", fontsize=8, fontweight='bold', zorder=6
        )

    # Yema Apical (punta de la planta)
    ax.plot(0, altura_acumulada + 0.5, marker='^', color='#c8e6c9', markersize=12, zorder=5)
    
    # Ajustes de límites y ocultar ejes
    ax.set_xlim(-8, 8)
    ax.set_ylim(-2, altura_acumulada + 4)
    ax.axis('off')
    
    st.pyplot(fig, use_container_width=True)
