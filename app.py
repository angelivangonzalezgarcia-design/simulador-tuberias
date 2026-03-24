# ----------------------
# ANIMACIÓN DEL FLUJO COMPLETO
# ----------------------
st.subheader("🌊 Simulación del Flujo Completo")

fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.set_xlim(0,10)
ax2.set_ylim(0,4)
ax2.axis('off')

# partículas a lo largo de todo el sistema
particles = np.linspace(0,10,40)

placeholder = st.empty()

for _ in range(80):
    ax2.clear()
    ax2.set_xlim(0,10)
    ax2.set_ylim(0,4)
    ax2.axis('off')

    # Tuberías (estructura completa)
    ax2.plot([0,2],[2,2], linewidth=4)
    ax2.plot([2,4],[2,3], linewidth=4)
    ax2.plot([2,4],[2,2], linewidth=4)
    ax2.plot([2,4],[2,1], linewidth=4)
    ax2.plot([4,8],[3,3], linewidth=4)
    ax2.plot([4,8],[2,2], linewidth=4)
    ax2.plot([4,8],[1,1], linewidth=4)
    ax2.plot([8,10],[3,2], linewidth=4)
    ax2.plot([8,10],[2,2], linewidth=4)
    ax2.plot([8,10],[1,2], linewidth=4)

    # velocidad base (depende del caudal total)
    base_speed = Q_total * 50

    particles = (particles + base_speed) % 10

    x_vals = []
    y_vals = []

    for x in particles:

        # Entrada
        if x < 2:
            y = 2

        # División
        elif x < 4:
            frac = (x - 2)/2
            y = 2 + np.random.choice([frac, 0, -frac])

        # Paralelo
        elif x < 8:
            branch = np.random.choice([1,2,3])
            y = {1:3, 2:2, 3:1}[branch]

        # Unión
        else:
            frac = (x - 8)/2
            y = 3 - frac if np.random.rand() < 0.33 else (1 + frac if np.random.rand() < 0.5 else 2)

        x_vals.append(x)
        y_vals.append(y)

    ax2.scatter(x_vals, y_vals, s=20)

    placeholder.pyplot(fig2)
    time.sleep(0.05)
