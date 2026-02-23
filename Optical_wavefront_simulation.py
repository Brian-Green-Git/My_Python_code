# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 12:29:58 2026

@author: brian green
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  

theta = 90
theta_val = np.deg2rad(theta)
class laser:
    def __init__ (self):
        self.power = 1
        self.wavelengh = 633E-9
        self.polarization = (1/np.sqrt(2)) * np.array([[1],
                                                       [0]])

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

laser_obj = laser()

pol_obj = polariser(theta_val)

print(f"initial input polarization:\n{laser_obj.polarization}")
print(f"\nPassing through polarizer at angle = {theta}")

# out = np.matmul(pol_obj.pol_axis,laser_obj.polarization)
out = pol_obj.linear_polarizer @ laser_obj.polarization
out = out / np.linalg.norm(out)

df = pd.DataFrame(out)

pol_wavefront_obj = polarization_of_wavefront()

polarization_df = pol_wavefront_obj.values(df.iloc[0], df.iloc[1])

print("\npolarization on each analyzer:")
print(f"{polarization_df.iloc[0]}\n")
