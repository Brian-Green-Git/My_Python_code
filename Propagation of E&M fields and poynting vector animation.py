import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Physical parameters
c = 1.0
k = 2 * np.pi
omega = c * k

# Space & time
z = np.linspace(-0.1, 2, 400)
dt = 0.05

# Figure setup
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 2)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
ax.set_xlabel("Propagation (z)")
ax.set_ylabel("B-field")
ax.set_zlabel("E-field")


# Field lines
E_line, = ax.plot([], [], [], color='blue', lw=2, alpha = 0.5, label='B-field')
B_line, = ax.plot([], [], [], color='red', lw=2, label='E-field')

# Poynting vector
ax.quiver(0, 0, 0, 2, 0, 0, color='green', linewidth=2, label='Propagation')

# Static wavefront marker
theta = np.linspace(0, 2*np.pi, 200)
r = 1.2
z0 = 0.0
ax.plot(np.full_like(theta, z0), r * np.cos(theta), r * np.sin(theta), color='green', lw=2)
ax.plot([z0, z0], [-1.2, 1.2], [0, 0], color='blue', lw=2)
ax.plot([z0, z0], [0, 0], [-1.2, 1.2], color='red', lw=2)

# Create wavefront disc (we’ll animate this)
phi = np.linspace(0, 2*np.pi, 40)
circle_r = 0.8
x_circ = np.zeros_like(phi)
y_circ = circle_r * np.cos(phi)
z_circ = circle_r * np.sin(phi)

verts = [list(zip(x_circ, y_circ, z_circ))]
wavefront = Poly3DCollection(verts, alpha=0.0001, color='purple')
ax.add_collection3d(wavefront)


#%%

ax.legend()

# --- Animation function ---
def update(frame):
    t = frame * dt

    # E and B fields
    E = np.cos(k*z - omega*t)
    B = np.cos(k*z - omega*t)

    E_line.set_data(z, E)
    E_line.set_3d_properties(np.zeros_like(z) - 0.2)
    B_line.set_data(z, np.zeros_like(z) + 0.25)
    B_line.set_3d_properties(B)

    #%%

    # Forward propagation
    z_pos = (t * c) % 2
    
    # Rocking angles (zero-mean)
    tilt_y = 10 * np.sin(0.7 * t)
    tilt_z = 0.4 * np.sin(0.7 * t + np.pi/2)
    
    
    # --- Local propagation (Poynting) vector ---
    
    # Start with unit vector along x
    Sx, Sy, Sz = 1.0, 0.0, 0.0
    
    # Rotate same as wavefront (y-axis)
    Sx1 =  Sx * np.cos(tilt_y) + Sz * np.sin(tilt_y)
    Sy1 =  Sy
    Sz1 = -Sx * np.sin(tilt_y) + Sz * np.cos(tilt_y)
    
    # Rotate same as wavefront (z-axis)
    Sx2 = Sx1 * np.cos(tilt_z) - Sy1 * np.sin(tilt_z)
    Sy2 = Sx1 * np.sin(tilt_z) + Sy1 * np.cos(tilt_z)
    Sz2 = Sz1
    
    
    S_vec = ax.quiver(
        z_pos, 0, 0,       # anchored at wavefront center
        0.2 * Sx2, 0.9 * Sy2, 0.9 * Sz2,
        color='purple',
        linewidth=1,
        arrow_length_ratio=0.2,
        label='Local propagation'
    )
    # S_vec.remove()

   
    #%%

    return E_line, B_line, S_vec

ani = FuncAnimation(fig, update, frames=400, interval=1)

plt.show()

