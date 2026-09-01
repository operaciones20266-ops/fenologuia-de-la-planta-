import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Registro de Planta", layout="centered")

st.title("🌱 Registro de Crecimiento de Planta")
st.write("Ingresa los datos para ver crecer el tallo y sus nudos.")

# Inicializar historial en la sesión
if "nudos" not in st.session_state:
    st.session_state["nudos"] = [
        {"nudo": "Nudo 1", "longitud": 5.0, "grosor": 8},
        {"nudo": "Nudo 2", "longitud": 8.5, "grosor": 7},
        {"nudo": "Nudo 3", "longitud": 6.0, "grosor": 5}
    ]

# Layout de 2 columnas
col1, col2 = st.columns([1, 1])

with col2:
    st.subheader("📝 Registrar Nuevo Nudo")
    nombre_nudo = f"Nudo {len(st.session_state['nudos']) + 1}"
    st.text(f"Registrando: {nombre_nudo}")
    
    longitud = st.number_input("Longitud del entrenudo (cm):", min_value=0.5, value=4.0, step=0.5)
    grosor = st.number_input("Grosor del tallo (mm):", min_value=1, value=5, step=1)
    
    if st.button("➕ Agregar a la Planta"):
        st.session_state["nudos"].append({
            "nudo": nombre_nudo,
            "longitud": longitud,
            "grosor": grosor
        })
        st.success(f"{nombre_nudo} agregado con éxito.")
        st.rerun()

with col1:
    st.subheader("📊 Vista de la Planta")
    
    # Dibujar la planta apilada con Matplotlib
    fig, ax = plt.subplots(figsize=(3, 6))
    
    bottom = 0
    colores = ['#2e7d32', '#388e3c', '#43a047', '#4caf50', '#66bb6a', '#81c784']
    
    for i, item in enumerate(st.session_state["nudos"]):
        color = colores[i % len(colores)]
        
        # Dibujar entrenudo (tallo)
        ax.bar("Planta", item["longitud"], bottom=bottom, width=0.3, color=color, edgecolor="black")
        
        # Punto del nudo
        posicion_nudo = bottom + item["longitud"]
        ax.plot(0, posicion_nudo, marker='o', color='brown', markersize=8)
        
        # Etiqueta del nudo
        ax.text(0.2, posicion_nudo, f" {item['nudo']} ({item['longitud']} cm)", va="center", fontsize=9)
        
        bottom += item["longitud"]
        
    ax.set_ylabel("Altura acumulada (cm)")
    ax.set_ylim(0, max(bottom + 5, 20))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)
