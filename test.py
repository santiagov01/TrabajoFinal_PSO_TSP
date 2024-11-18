import matplotlib.pyplot as plt
import numpy as np

# Activar el modo interactivo
plt.ion()

# Crear la primera figura
fig1, ax1 = plt.subplots()
x = np.linspace(0, 10, 100)
y = np.sin(x)
line1, = ax1.plot(x, y)
ax1.set_title('Ventana 1: Seno')

# Crear la segunda figura
fig2, ax2 = plt.subplots()
y2 = np.cos(x)
line2, = ax2.plot(x, y2)
ax2.set_title('Ventana 2: Coseno')

# Mostrar las ventanas
plt.show()

# Actualizar las ventanas en un bucle (por ejemplo, animación)
for i in range(100):
    # Cambiar los datos de la primera ventana (figura 1)
    y = np.sin(x + i / 10)
    line1.set_ydata(y)
    fig1.canvas.draw()  # Redibujar la ventana de la figura 1
    fig1.canvas.flush_events()  # Asegurarse de que los eventos se procesen

    # Cambiar los datos de la segunda ventana (figura 2)
    y2 = np.cos(x + i / 10)
    line2.set_ydata(y2)
    fig2.canvas.draw()  # Redibujar la ventana de la figura 2
    fig2.canvas.flush_events()  # Asegurarse de que los eventos se procesen

    plt.pause(0.001)  # Pausa para controlar la velocidad de actualización
