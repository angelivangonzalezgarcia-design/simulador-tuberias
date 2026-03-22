import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Simulador de Tuberías", layout="wide")

st.title("Simulación Interactiva de Flujo en Tuberías en Paralelo")

# INPUTS
st.sidebar.header("Parámetros")
Q_total = st.sidebar.slider("Caudal total (m3/s)", 0.001, 0.1, 0.02)
D = st.sidebar.slider("Diámetro (m)", 0.01, 0.5, 0.1)

valve1 = st.sidebar.slider("Válvula 1", 0.1, 1.0, 1.0)
valve2 = st.sidebar.slider("Válvula 2", 0.1, 1.0, 1.0)
valve3 = st.sidebar.slider("Válvula 3", 0.1, 1.0, 1.0)

# MODELO
rho = 1000
A = np.pi * (D/2)**2

K1, K2, K3 = 10/valve1, 10/valve2, 10/valve3
R1, R2, R3 = K1, K2, K3

Q1 = Q_total*(1/R1)/(1/R1+1/R2+1/R3)
Q2 = Q_total*(1/R2)/(1/R1+1/R2+1/R3)
Q3 = Q_total*(1/R3)/(1/R1+1/R2+1/R3)

v1, v2, v3 = Q1/A, Q2/A, Q3/A

# RESULTADOS
st.subheader("Resultados")
st.write(f"Q1={Q1:.4f}, Q2={Q2:.4f}, Q3={Q3:.4f}")
st.write(f"v1={v1:.2f}, v2={v2:.2f}, v3={v3:.2f}")

# ANIMACION
st.subheader("Visualización del flujo")
fig, ax = plt.subplots(figsize=(8,3))
ax.set_xlim(0,10)
ax.set_ylim(0,3)
ax.axis('off')

particles1 = np.linspace(0,10,15)
particles2 = np.linspace(0,10,15)
particles3 = np.linspace(0,10,15)

placeholder = st.empty()

for _ in range(60):
    ax.clear()
    ax.set_xlim(0,10)
    ax.set_ylim(0,3)
    ax.axis('off')

    ax.plot([0,10],[2.5,2.5])
    ax.plot([0,10],[1.5,1.5])
    ax.plot([0,10],[0.5,0.5])

    particles1 = (particles1 + v1*0.1) % 10
    particles2 = (particles2 + v2*0.1) % 10
    particles3 = (particles3 + v3*0.1) % 10

    ax.scatter(particles1, [2.5]*len(particles1))
    ax.scatter(particles2, [1.5]*len(particles2))
    ax.scatter(particles3, [0.5]*len(particles3))

    placeholder.pyplot(fig)
    time.sleep(0.05)

st.write("Más caudal = mayor velocidad visual del flujo")
