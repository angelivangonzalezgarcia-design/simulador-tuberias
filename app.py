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
# GEOMETRÍA
# ----------------------

# Entrada
x_in = np.linspace(0, 3, 50)
y_in = np.zeros_like(x_in)
z_in = np.zeros_like(x_in)

# Nodo división
x_split = 3

# Ramas
x_branch = np.linspace(3, 8, 50)
y1 = np.ones_like(x_branch) * 2
y2 = np.zeros_like(x_branch)
y3 = np.ones_like(x_branch) * -2
z = np.zeros_like(x_branch)

# Nodo unión
x_merge = 8

# Salida
x_out = np.linspace(8, 11, 50)
y_out = np.zeros_like(x_out)
z_out = np.zeros_like(x_out)

# ----------------------
# FIGURA
# ----------------------
fig = go.Figure()

# Entrada
fig.add_trace(go.Scatter3d(x=x_in, y=y_in, z=z_in,
                          mode='lines',
                          line=dict(width=10),
                          name='Entrada'))

# Nodo división
fig.add_trace(go.Scatter3d(x=[x_split], y=[0], z=[0],
                          mode='markers',
                          marker=dict(size=6),
                          name='Nodo división'))

# Ramas
fig.add_trace(go.Scatter3d(x=x_branch, y=y1, z=z,
                          mode='lines', line=dict(width=10),
                          name='Rama 1'))

fig.add_trace(go.Scatter3d(x=x_branch, y=y2, z=z,
                          mode='lines', line=dict(width=10),
                          name='Rama 2'))

fig.add_trace(go.Scatter3d(x=x_branch, y=y3, z=z,
                          mode='lines', line=dict(width=10),
                          name='Rama 3'))

# Nodo unión
fig.add_trace(go.Scatter3d(x=[x_merge], y=[0], z=[0],
                          mode='markers',
                          marker=dict(size=6),
                          name='Nodo unión'))

# Salida
fig.add_trace(go.Scatter3d(x=x_out, y=y_out, z=z_out,
                          mode='lines',
                          line=dict(width=10),
                          name='Salida'))

# ----------------------
# FLUJO (PARTÍCULAS)
# ----------------------

t = np.linspace(0, 1, 30)

# Entrada
fig.add_trace(go.Scatter3d(
    x=0 + t*3,
    y=np.zeros_like(t),
    z=np.zeros_like(t),
    mode='markers',
    marker=dict(size=4),
    name='Flujo entrada'
))

# Ramas
fig.add_trace(go.Scatter3d(x=3 + t*5, y=2*np.ones_like(t), z=0*t,
                          mode='markers', marker=dict(size=4),
                          name='Flujo rama 1'))

fig.add_trace(go.Scatter3d(x=3 + t*5, y=0*np.ones_like(t), z=0*t,
                          mode='markers', marker=dict(size=4),
                          name='Flujo rama 2'))

fig.add_trace(go.Scatter3d(x=3 + t*5, y=-2*np.ones_like(t), z=0*t,
                          mode='markers', marker=dict(size=4),
                          name='Flujo rama 3'))

# Salida
fig.add_trace(go.Scatter3d(
    x=8 + t*3,
    y=np.zeros_like(t),
    z=np.zeros_like(t),
    mode='markers',
    marker=dict(size=4),
    name='Flujo salida'
))

# Layout
fig.update_layout(
    scene=dict(
        xaxis_title='Longitud',
        yaxis_title='Distribución',
        zaxis_title='Altura'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------
# RESULTADOS
# ----------------------
st.subheader("📊 Resultados")
st.write(f"Q1 = {Q1:.4f} m³/s")
st.write(f"Q2 = {Q2:.4f} m³/s")
st.write(f"Q3 = {Q3:.4f} m³/s")

# ----------------------
# INTERPRETACIÓN
# ----------------------
st.subheader("🧠 Interpretación")
st.write("El sistema muestra la secuencia física: entrada → división → flujo en paralelo → unión → salida.")
st.write("El flujo se reparte según la resistencia hidráulica de cada rama.")
