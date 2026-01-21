import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Physical parameters (scaled units)
c = 1.0
k = 2 * np.pi
omega = c * k

# Space and time
z = np.linspace(-0.1, 2, 400)
dt = 0.05

# Figure
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 2)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)

ax.set_xlabel("Propagation (z)")
ax.set_ylabel("B-field")
ax.set_zlabel("E-field")

# Lines
E_line, = ax.plot([], [], [], color='blue', lw=2, label='B-field')
B_line, = ax.plot([], [], [], color='red', lw=2, label='E-field')

# Static Poynting vector
ax.quiver(
    0, 0, 0,
    2, 0, 0,
    color='green',
    linewidth=2,
    label='Propagation'
)


# ---- Wavefront marker (circle + cross) ----
theta = np.linspace(0, 2*np.pi, 200)
r = 1.2
z0 = 0.0

# Circle (wavefront)
ax.plot(
    np.full_like(theta, z0),
    r * np.cos(theta),
    r * np.sin(theta),
    color='green',
    lw=2
)

# Cross
ax.plot([z0, z0], [-1.2, 1.2], [0, 0], color='blue', lw=2)
ax.plot([z0, z0], [0, 0], [-1.2, 1.2], color='red', lw=2)



ax.legend()


def update(frame):
    t = frame * dt

    # Fields
    E = np.cos(k*z - omega*t)
    B = np.cos(k*z - omega*t)

    # Electric field oscillates in y, offset in B-direction
    E_line.set_data(z, E)
    E_line.set_3d_properties(np.zeros_like(z) - 0.2)

    # Magnetic field oscillates in x, offset in E-direction
    B_line.set_data(z, np.zeros_like(z) + 0.25)
    B_line.set_3d_properties(B)

    return E_line, B_line

ani = FuncAnimation(fig, update, frames=200, interval=40)
plt.show()
