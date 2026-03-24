import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador 3D Tuberías", layout="wide")

st.title("🔧 Simulador 3D: Sistema con División y Unión de Flujo")

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

# ----------------------
# GEOMETRÍA DEL SISTEMA
# ----------------------

# Entrada
x_main = np.linspace(0,2,20)
y_main = np.zeros_like(x_main)
z_main = np.zeros_like(x_main)

# División
x_branch = np.linspace(2,8,50)
y1 = np.linspace(0,2,50)
y2 = np.linspace(0,0,50)
y3 = np.linspace(0,-2,50)
z = np.zeros_like(x_branch)

# Unión
x_merge = np.linspace(8,10,20)
y_merge = np.zeros_like(x_merge)
z_merge = np.zeros_like(x_merge)

fig = go.Figure()

# Línea principal entrada
fig.add_trace(go.Scatter3d(x=x_main,y=y_main,z=z_main,mode='lines',line=dict(width=8),name='Entrada'))

# Ramas
fig.add_trace(go.Scatter3d(x=x_branch,y=y1,z=z,mode='lines',line=dict(width=8),name='Tubería 1'))
fig.add_trace(go.Scatter3d(x=x_branch,y=y2,z=z,mode='lines',line=dict(width=8),name='Tubería 2'))
fig.add_trace(go.Scatter3d(x=x_branch,y=y3,z=z,mode='lines',line=dict(width=8),name='Tubería 3'))

# Salida
fig.add_trace(go.Scatter3d(x=x_merge,y=y_merge,z=z_merge,mode='lines',line=dict(width=8),name='Salida'))

# ----------------------
# PARTÍCULAS (FLUJO)
# ----------------------

t = np.linspace(0,10,30)

# entrada
fig.add_trace(go.Scatter3d(x=t*0.2,y=np.zeros_like(t),z=np.zeros_like(t),mode='markers',marker=dict(size=3),name='Flujo entrada'))

# ramas
fig.add_trace(go.Scatter3d(x=t*0.6+2,y=np.linspace(0,2,30),z=np.zeros_like(t),mode='markers',marker=dict(size=3),name='Flujo 1'))
fig.add_trace(go.Scatter3d(x=t*0.6+2,y=np.zeros_like(t),z=np.zeros_like(t),mode='markers',marker=dict(size=3),name='Flujo 2'))
fig.add_trace(go.Scatter3d(x=t*0.6+2,y=np.linspace(0,-2,30),z=np.zeros_like(t),mode='markers',marker=dict(size=3),name='Flujo 3'))

# salida
fig.add_trace(go.Scatter3d(x=t*0.2+8,y=np.zeros_like(t),z=np.zeros_like(t),mode='markers',marker=dict(size=3),name='Flujo salida'))

fig.update_layout(scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'),margin=dict(l=0,r=0,b=0,t=0))

st.plotly_chart(fig, use_container_width=True)

# ----------------------
# INTERPRETACIÓN
# ----------------------
st.subheader("🧠 Análisis")
st.write("El flujo entra por una tubería principal, se divide en tres ramas en paralelo y posteriormente se vuelve a unir.")
st.write("La distribución del flujo depende de la resistencia de cada válvula.")
