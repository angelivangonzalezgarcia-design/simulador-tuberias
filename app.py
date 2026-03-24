import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador 3D Tuberías", layout="wide")

st.title("🔧 Simulador 3D: Sistema de Tuberías en Paralelo")

# ----------------------
# CONTROLES
# ----------------------
st.sidebar.header("⚙️ Parámetros")
Q_total = st.sidebar.slider("Caudal total (m³/s)", 0.001, 0.1, 0.02)
D = st.sidebar.slider("Diámetro (m)", 0.01, 0.5, 0.1)

valve1 = st.sidebar.slider("Válvula 1", 0.1, 1.0, 1.0)
valve2 = st.sidebar.slider("Válvula 2", 0.1, 1.0, 1.0)
valve3 = st.sidebar.slider("Válvula 3", 0.1, 1.0, 1.0)

# ----------------------
# MODELO
# ----------------------
rho = 1000
A = np.pi * (D/2)**2

K1, K2, K3 = 10/valve1, 10/valve2, 10/valve3

Q1 = Q_total*(1/K1)/(1/K1+1/K2+1/K3)
Q2 = Q_total*(1/K2)/(1/K1+1/K2+1/K3)
Q3 = Q_total*(1/K3)/(1/K1+1/K2+1/K3)

v1, v2, v3 = Q1/A, Q2/A, Q3/A

# ----------------------
# RESULTADOS
# ----------------------
st.subheader("📊 Resultados")
st.write(f"Q1={Q1:.4f}, Q2={Q2:.4f}, Q3={Q3:.4f}")
st.write(f"v1={v1:.2f}, v2={v2:.2f}, v3={v3:.2f}")

# ----------------------
# 3D VISUALIZACIÓN
# ----------------------
st.subheader("🌐 Simulación 3D del Sistema")

x = np.linspace(0,10,50)

y_levels = [2, 0, -2]
velocities = [v1, v2, v3]

fig = go.Figure()

for i,y in enumerate(y_levels):
    z = np.zeros_like(x)
    fig.add_trace(go.Scatter3d(
        x=x,
        y=[y]*len(x),
        z=z,
        mode='lines',
        line=dict(width=10),
        name=f"Tubería {i+1}"
    ))

    # partículas
    xp = np.linspace(0,10,15)
    zp = np.zeros_like(xp)
    fig.add_trace(go.Scatter3d(
        x=xp,
        y=[y]*len(xp),
        z=zp,
        mode='markers',
        marker=dict(size=4),
        name=f"Flujo {i+1}"
    ))

fig.update_layout(
    scene=dict(
        xaxis_title='Longitud',
        yaxis_title='Ramas',
        zaxis_title='Altura'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------
# INTERPRETACIÓN
# ----------------------
st.subheader("🧠 Análisis")
st.write("El sistema se representa en 3D para visualizar las ramas en paralelo.")
st.write("La distribución de flujo depende de la resistencia de cada tubería.")
st.write("Mayor velocidad implica mayor transporte de fluido en esa rama.")
