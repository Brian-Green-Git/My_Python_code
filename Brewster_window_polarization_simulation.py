# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:25:42 2026

@author: 224252927
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 12:29:58 2026

@author: brian green
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  

theta = 0
theta_val = np.deg2rad(theta)
n_1 = 1
n_2 = 1.5

theta_I = np.deg2rad(np.arange(0, 90, 1))


theta_R = np.arange(5, 100, 5)

class laser:
    def __init__ (self):
        self.power = 1
        self.wavelengh = 633E-9
        self.polarization = (1/np.sqrt(2)) * np.array([[1],
                                                       [1]])

class polariser:
    def __init__(self, inp):        
        theta = inp
        self.linear_polarizer = np.array([[np.cos(theta)**2, np.cos(theta)*np.sin(theta)],
                                          [np.cos(theta)*np.sin(theta), np.sin(theta)**2]])
        
        self.right_circular_polarizer = 1/2 * np.array([[1, 1j],
                                                        [-1j, 1]])
        
        self.left_curcular_polarizer = 1/2 * np.array([[1, -1j],
                                                       [1j, 1]])

class polarization_of_wavefront:
    
    def values(self, H_in, V_in):
        H = H_in
        V = V_in
        D = (1/np.sqrt(2))*(H + V)
        A = (1/np.sqrt(2))*(H - V)
        R = (1/np.sqrt(2))*(H - (1j)*V)
        L = (1/np.sqrt(2))*(H + (1j)*V)

        self.arr = [V, D, A, R, L]
        
        I_H = abs(H)**2
        I_V = abs(V)**2
        I_D = abs(D)**2
        I_A = abs(A)**2
        I_R = abs(R)**2
        I_L = abs(L)**2
 
        self.df = pd.DataFrame({
            "Horizontal": I_H,
            "Vertical": I_V,
            "Diagonal": I_D,
            "Antidiagonal": I_A,
            "Right": I_R,
            "Left": I_L
            })

        return(self.df)
    
#----------------------------------------------------------------

def glass_plate(theta_I):
    theta_T = np.arcsin((n_1 / n_2) * np.sin(theta_I))
    
    R_s = np.abs(
        (n_1 * np.cos(theta_I) - n_2 * np.cos(theta_T)) /
        (n_1 * np.cos(theta_I) + n_2 * np.cos(theta_T))
    )**2

    R_p = np.abs(
        (n_2 * np.cos(theta_I) - n_1 * np.cos(theta_T)) /
        (n_2 * np.cos(theta_I) + n_1 * np.cos(theta_T))
    )**2

    return R_p, R_s
# __________________________________________________________________

Rp, Rs = glass_plate(theta_I)

# Output_S_pol = np.array()
# Output_P_pol = np.array()

#---------------------------------------------------------

laser_obj = laser()

pol_obj = polariser(theta_val)

E_in = laser_obj.polarization

E_s = E_in[0]  # s-component
E_p = E_in[1]  # p-component



I_after_pol = []

for i in range(len(theta_I)):
    
    # Reflection Jones matrix
    # J_ref = np.array([
    #     [np.sqrt(Rs[i]), 0],
    #     [0, np.sqrt(Rp[i])]
    # ])
    
    J_ref = np.array([
    [Rs[i], 0],
    [0, Rp[i]]
])
    
    # Reflected field
    E_ref = J_ref @ E_in
    
    # print(f"E_ref = {E_ref}")
    
    # Apply polarizer
    E_out = pol_obj.linear_polarizer @ E_ref
    
    # Intensity
    I_out = np.linalg.norm(E_out)**2
    
    I_after_pol.append(I_out)
    
    
print(f"Polarization is: {theta}\n")
for i in  range(0, len(theta_I), 5):
    print(f"I_out_{i} = { I_after_pol[i]}")
    
plt.plot(np.rad2deg(theta_I), I_after_pol, label="After polarizer")
plt.xlabel("Incident Angle (degrees)")
plt.ylabel("Intensity")
plt.legend()
plt.grid()
plt.show()    

#%%

for i in range(0, len(theta_R)):
    Out_s = Rs[i] * E_s
    Out_p = Rp[i] * E_p


#%%
plt.plot(np.rad2deg(theta_I), Rp, label="Rp (p-pol -- Vertial polarization)")
plt.plot(np.rad2deg(theta_I), Rs, label="Rs (s-pol -- Horizaontal polarization)")
plt.xlabel("Incident Angle (degrees)")
plt.ylabel("Reflectance")
plt.legend()
plt.grid()
plt.show()

#%%

print(f"initial input polarization:\n{laser_obj.polarization}")
print(f"\nPassing through polarizer at angle = {theta}")

out = pol_obj.linear_polarizer @ laser_obj.polarization
out = out / np.linalg.norm(out)

df = pd.DataFrame(out)

pol_wavefront_obj = polarization_of_wavefront()

polarization_df = pol_wavefront_obj.values(df.iloc[0], df.iloc[1])

print("\npolarization on each analyzer:")
print(f"{polarization_df.iloc[0]}\n")
# print("polarization_df.iloc[0]:.2f")  # 2 decimal places