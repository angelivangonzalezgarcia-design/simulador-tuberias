import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Simulador de Tuberías", layout="wide")

st.title("🔧 Simulador Profesional: Sistema de Tuberías en Paralelo")

# ----------------------
# SIDEBAR (CONTROLES)
# ----------------------
st.sidebar.header("⚙️ Parámetros del Sistema")

Q_total = st.sidebar.slider("Caudal total (m³/s)", 0.001, 0.1, 0.02)
D = st.sidebar.slider("Diámetro (m)", 0.01, 0.5, 0.1)

valve1 = st.sidebar.slider("Apertura Válvula 1", 0.1, 1.0, 1.0)
valve2 = st.sidebar.slider("Apertura Válvula 2", 0.1, 1.0, 1.0)
valve3 = st.sidebar.slider("Apertura Válvula 3", 0.1, 1.0, 1.0)

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
st.subheader("📊 Resultados del Sistema")
col1, col2, col3 = st.columns(3)

col1.metric("Tubería 1", f"Q={Q1:.4f} m³/s\nV={v1:.2f} m/s")
col2.metric("Tubería 2", f"Q={Q2:.4f} m³/s\nV={v2:.2f} m/s")
col3.metric("Tubería 3", f"Q={Q3:.4f} m³/s\nV={v3:.2f} m/s")

# ----------------------
# DIAGRAMA PROFESIONAL
# ----------------------
st.subheader("🛠️ Diagrama del Sistema")

fig, ax = plt.subplots(figsize=(10,4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')

# Nodo entrada
ax.scatter(1,2, s=200)
ax.text(0.5,2,"Entrada", fontsize=10)

# Nodo salida
ax.scatter(9,2, s=200)
ax.text(9.1,2,"Salida", fontsize=10)

# Tuberías
ys = [3,2,1]
flows = [v1,v2,v3]
Qs = [Q1,Q2,Q3]

for i,y in enumerate(ys):
    ax.plot([1,9],[y,y], linewidth=3)
    ax.text(4.5,y+0.2,f"Q={Qs[i]:.3f}")

# ----------------------
# ANIMACIÓN
# ----------------------
st.subheader("🌊 Simulación del Flujo")

fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.set_xlim(0,10)
ax2.set_ylim(0,4)
ax2.axis('off')

particles = [np.linspace(1,9,20) for _ in range(3)]
placeholder = st.empty()

for _ in range(60):
    ax2.clear()
    ax2.set_xlim(0,10)
    ax2.set_ylim(0,4)
    ax2.axis('off')

    for i,y in enumerate(ys):
        ax2.plot([1,9],[y,y], linewidth=3)
        particles[i] = (particles[i] + flows[i]*0.1) % 8 + 1
        ax2.scatter(particles[i], [y]*len(particles[i]))

    placeholder.pyplot(fig2)
    time.sleep(0.05)

# ----------------------
# INTERPRETACIÓN
# ----------------------
st.subheader("🧠 Análisis")
st.write("- El flujo se distribuye según la resistencia hidráulica.")
st.write("- Mayor apertura de válvula → menor resistencia → mayor caudal.")
st.write("- La animación muestra el comportamiento dinámico del fluido.")

