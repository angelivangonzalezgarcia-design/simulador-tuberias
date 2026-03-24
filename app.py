import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Simulador de Tuberías", layout="wide")

st.title("🔧 Simulación de Flujo en Tuberías en Paralelo")

# ----------------------
# CONTROLES
# ----------------------
st.sidebar.header("⚙️ Parámetros del Sistema")

Q_total = st.sidebar.slider("Caudal total (m³/s)", 0.001, 0.1, 0.02)
D = st.sidebar.slider("Diámetro de tuberías (m)", 0.01, 0.5, 0.1)

valve1 = st.sidebar.slider("Apertura válvula 1", 0.1, 1.0, 1.0)
valve2 = st.sidebar.slider("Apertura válvula 2", 0.1, 1.0, 1.0)
valve3 = st.sidebar.slider("Apertura válvula 3", 0.1, 1.0, 1.0)

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

col1, col2, col3 = st.columns(3)

col1.metric("Tubería 1", f"Q={Q1:.4f} m³/s\nV={v1:.2f} m/s")
col2.metric("Tubería 2", f"Q={Q2:.4f} m³/s\nV={v2:.2f} m/s")
col3.metric("Tubería 3", f"Q={Q3:.4f} m³/s\nV={v3:.2f} m/s")

# ----------------------
# DIAGRAMA DEL SISTEMA
# ----------------------
st.subheader("🛠️ Sistema de Tuberías")

fig, ax = plt.subplots(figsize=(10,4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')

# Entrada
ax.plot([0,2],[2,2], linewidth=4)

# División
ax.plot([2,4],[2,3], linewidth=4)
ax.plot([2,4],[2,2], linewidth=4)
ax.plot([2,4],[2,1], linewidth=4)

# Paralelo
ax.plot([4,8],[3,3], linewidth=4)
ax.plot([4,8],[2,2], linewidth=4)
ax.plot([4,8],[1,1], linewidth=4)

# Unión
ax.plot([8,10],[3,2], linewidth=4)
ax.plot([8,10],[2,2], linewidth=4)
ax.plot([8,10],[1,2], linewidth=4)

st.pyplot(fig)

# ----------------------
# ANIMACIÓN DEL FLUJO
# ----------------------
st.subheader("🌊 Simulación del Flujo")

fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.set_xlim(0,10)
ax2.set_ylim(0,4)
ax2.axis('off')

particles1 = np.linspace(4,8,20)
particles2 = np.linspace(4,8,20)
particles3 = np.linspace(4,8,20)

placeholder = st.empty()

for _ in range(60):
    ax2.clear()
    ax2.set_xlim(0,10)
    ax2.set_ylim(0,4)
    ax2.axis('off')

    # Tuberías
    ax2.plot([0,2],[2,2])
    ax2.plot([2,4],[2,3])
    ax2.plot([2,4],[2,2])
    ax2.plot([2,4],[2,1])
    ax2.plot([4,8],[3,3])
    ax2.plot([4,8],[2,2])
    ax2.plot([4,8],[1,1])
    ax2.plot([8,10],[3,2])
    ax2.plot([8,10],[2,2])
    ax2.plot([8,10],[1,2])

    # Movimiento
    particles1 = (particles1 + v1*0.2) % 4 + 4
    particles2 = (particles2 + v2*0.2) % 4 + 4
    particles3 = (particles3 + v3*0.2) % 4 + 4

    ax2.scatter(particles1, [3]*len(particles1))
    ax2.scatter(particles2, [2]*len(particles2))
    ax2.scatter(particles3, [1]*len(particles3))

    placeholder.pyplot(fig2)
    time.sleep(0.05)

# ----------------------
# INTERPRETACIÓN
# ----------------------
st.subheader("🧠 Interpretación")

st.write("El flujo entra por una tubería principal, se divide en tres ramas en paralelo y posteriormente se vuelve a unir.")
st.write("La distribución del caudal depende de la resistencia de cada válvula.")
