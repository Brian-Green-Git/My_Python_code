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

n_1 = 1
n_2 = 2

theta_I = np.deg2rad(np.arange(0, 90, 1))

I_after_pol = []

I_transmitted = []

#%% Objects 
class laser:
    def __init__ (self):
        self.power = 20e-3  # 20 mW
        self.waist = 0.008   # 1mm
        self.wavelengh = 633E-9
        self.polarization = (1/np.sqrt(2)) * np.array([[1],  #Horizontal
                                                       [1]]) #Vertical

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
            "Horizontal": [I_H],
            "Vertical": [I_V],
            "Diagonal": [I_D],
            "Antidiagonal": [I_A],
            "Right": [I_R],
            "Left": [I_L]
        })

        return(self.df)
    
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
    
#%% Creation of objects 
laser_obj = laser()

E_in = laser_obj.polarization

pol1 = polariser(np.deg2rad(0))
pol2 = polariser(np.deg2rad(0))

P_in = laser_obj.power

beam_A = np.pi * (laser_obj.waist)**2 

#%% Defining our polarization states from an unpolarized beam
#%%
# Defing the first polarizer angle and applying it to the input field 

E_out_Pol_1 = pol1.linear_polarizer @ E_in

df = pd.DataFrame(E_out_Pol_1)

pol_wavefront_obj = polarization_of_wavefront()

polarization_df = pol_wavefront_obj.values(E_out_Pol_1[0,0], E_out_Pol_1[1,0])

print(f"\nHorizontal Basis polarization intensity: {polarization_df['Horizontal']}\n")

#%%
# Defing the second polariser angle and applying it to the output field from polarizer 1

E_out_Pol_2 = pol2.linear_polarizer @ E_out_Pol_1

df = pd.DataFrame(E_out_Pol_2)

pol_wavefront_obj = polarization_of_wavefront()

polarization_df = pol_wavefront_obj.values(E_out_Pol_2[0,0], E_out_Pol_2[1,0])

print(f"\nHorizontal Basis polarization intensity: {polarization_df['Horizontal']}\n")

#%% Passing E field onto the glass plate

Rp, Rs = glass_plate(theta_I)

I_after_pol = [] 

val = 0
analyzer = polariser(np.deg2rad(val))

for i in range(len(theta_I)):
    
    # Reflection Jones matrix
    J_ref = np.array([
        [np.sqrt(Rs[i]), 0],
        [0, np.sqrt(Rp[i])]
    ])
    
    # Reflected field
    E_ref = J_ref @ E_out_Pol_2 
    
    E_out = analyzer.linear_polarizer @ E_ref
    
    # Intensity
    I_out = np.linalg.norm(E_out)**2
    
    if I_out < 1E-12:
        I_out = 0
    
    I_after_pol.append(I_out)
    
    
    
for i in  range(0, len(theta_I), 5):
    print(f"I_out_{i} = { I_after_pol[i]}")

plt.figure()
plt.plot(np.rad2deg(theta_I), I_after_pol)
plt.title(f"Reflected light After polarizer set at {val}")
plt.xlabel("Incident Angle (degrees)")
plt.ylabel("Intensity after polarizer")
plt.grid()
plt.show()    

#%%

Power = []

print("\n\n")

for i in range(len(I_after_pol)):
    P_out = I_after_pol[i] / beam_A
    Power.append(P_out)

for i in  range(0, len(theta_I), 5):
    print(f"power_out_{i} = {Power[i]}")
   
    
#%% P and S componenets spilt 

E_s = E_in[0]
E_p = E_in[1]

I_s = Rs #* np.abs(E_s)**2
# I_p = Rp #* np.abs(E_p)**2

T_s = 1 - Rs
# T_p = 1 - Rp

plt.figure()
# plt.plot(np.rad2deg(theta_I), I_p, label="Rp (p-pol -- V)")
plt.plot(np.rad2deg(theta_I), I_s, label="Rs (s-pol -- H)")

# plt.plot(np.rad2deg(theta_I), T_p, label="Tp (p-pol -- V)")
plt.plot(np.rad2deg(theta_I), T_s, label="Ts (s-pol -- H)")
plt.xlabel("Incident Angle (degrees)")
plt.ylabel("Reflected Intensity")
plt.title("Reflected light After polarizer set at 0")
plt.legend()
plt.grid()
plt.show()
