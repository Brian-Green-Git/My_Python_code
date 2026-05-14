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

#%%

n_1 = 1
n_2 = 1.5

theta_I = np.deg2rad(np.arange(0, 91, 1))

I_after_pol = []

I_transmitted = []

#%% Objects 
class laser:
    def __init__ (self):
        self.power = 1000  # 2000 microW
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
pol2 = polariser(np.deg2rad(45))

P_in = laser_obj.power

beam_A = np.pi * (laser_obj.waist)**2 

#%% Defining our polarization states from an unpolarized beam

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

P_after_pol = np.linalg.norm(E_out_Pol_2)**2 * P_in

#%% Passing E field onto the glass plate

Rp, Rs = glass_plate(theta_I)

I_after_pol_H_R = [] 
I_after_pol_V_R = [] 
I_after_pol_H_T = [] 
I_after_pol_V_T = [] 

def intensity_from_glass_plate(val):
    analyzer = polariser(np.deg2rad(val))
    I_after_pol = []

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
        
    return I_after_pol
    
val = 0    
I_after_pol_H_R = intensity_from_glass_plate(val)

# plt.figure()
# plt.plot(np.rad2deg(theta_I), I_after_pol_H_R)
# plt.title(f"Reflected light After polarizer set at {val}")
# plt.xlabel("Incident Angle (degrees)")
# plt.ylabel("Intensity after polarizer")
# plt.grid()
# plt.show()    

val = 90
I_after_pol_V_R = intensity_from_glass_plate(val)

# plt.figure()
# plt.plot(np.rad2deg(theta_I), I_after_pol_V_R)
# plt.title(f"Reflected light After polarizer set at {val}")
# plt.xlabel("Incident Angle (degrees)")
# plt.ylabel("Intensity after polarizer")
# plt.grid()
# plt.show()    
    
#%%

Power_H_R = (P_in) * Rs
Power_H_T = (P_in - 300) * (1 - Rs)

Power_V_R = P_in * Rp
Power_V_T = (P_in - 50) * (1 - Rp)

def plot_H():
    plt.plot(np.rad2deg(theta_I), Power_H_R, label = 'H - Reflected - Theoretical', color = 'yellow')
    plt.plot(np.rad2deg(theta_I), Power_H_T, label = 'H - Transmitted - Theoretical', color = 'green')
    plt.title(f"Reflected light After polarizer set at {val}")
    plt.xlabel("Incident Angle (degrees)")
    plt.ylabel("Intensity after polarizer")
    plt.legend()
# plt.figure()
# plot_H()
# plt.grid()
# plt.show()    


def plot_V():
    plt.plot(np.rad2deg(theta_I), Power_V_R, label = 'V - Reflected - Theoretical', color = 'yellow')
    plt.plot(np.rad2deg(theta_I), Power_V_T, label = 'V - Transmitted - Theoretical', color = 'green')
    plt.title(f"Reflected light After polarizer set at {val}")
    plt.xlabel("Incident Angle (degrees)")
    plt.ylabel("Intensity after polarizer")
    plt.legend()
# plt.figure()
# plot_V()
# plt.grid()
# plt.show()


#%% P and S componenets spilt 

# E_s = E_in[0]
# E_p = E_in[1]

# I_s = Rs / beam_A 
# I_p = Rp / beam_A

# T_s = 1/ beam_A - (Rs / beam_A)
# T_p = 1/ beam_A - (Rp / beam_A)

# plt.figure()
# plt.plot(np.rad2deg(theta_I), I_p, label="Rp (p-pol -- V)")
# plt.plot(np.rad2deg(theta_I), I_s, label="Rs (s-pol -- H)")

# plt.plot(np.rad2deg(theta_I), T_p, label="Tp (p-pol -- V)")
# plt.plot(np.rad2deg(theta_I), T_s, label="Ts (s-pol -- H)")
# plt.xlabel("Incident Angle (degrees)")
# plt.ylabel("Reflected Intensity")
# plt.title("Reflected light After polarizer set at 0")
# plt.legend()
# plt.grid()
# plt.show()

#%% importing experimental data

df2 = pd.read_excel(r"C:\Users\Photonics LAB\Documents\Experimental results\Brewster experiment\Brewster_Data.xlsx")

df2.shape

Initial_p = df2["Initial_power"]
Power_p1 = df2["Power_p1"]
Power_p2 = df2["Power_p2"]
Power_Io = df2["Power_Io_mW"]  # Io power in mW

#%% isolating angular reuslts from extra columns containing intial power and changed powers after polarizers

Exp_df = df2.iloc[:,[0,1,2,3,4]]

Exp_df.shape

#%% plotting experimental results

angles = Exp_df['Angle']
Ref_P_H = Exp_df['Reflected_power_H_microW']
Trans_P_H = Exp_df['Transmitted_power_H_microW']

Ref_P_V = Exp_df['Reflected_power_V_microW']
Trans_P_V = Exp_df['Transmitted_power_V_microW']


# #plotting Horizontally polarized Reflected power VS angle
# plt.figure()
# plt.scatter(angles, Ref_P_H, color = 'blue')
# plt.plot(angles, Ref_P_H, color = "blue", zorder = 1, label = "H - Reflected - Experimental")
# # plt.plot(np.rad2deg(theta_I), Power_H_R, label = 'H - Reflected - Theoretical', color = 'black')
# plt.title('Plot of Horizontally Polarized Reflected Power VS Angle of Incidence')
# plt.xlabel('Angle (degrees)')
# plt.ylabel('Power (μW)')
# plt.legend()
# plt.grid()
# plt.show()


#plotting Horizontally polarized Reflected and Transmitted VS angle
plt.figure()
plot_H()
plt.scatter(angles, Trans_P_H, color = 'red')
plt.plot(angles, Trans_P_H, color = "red", zorder = 1, label = "H - Reflected - Experimental")
plt.scatter(angles, Ref_P_H, color = 'blue')
plt.plot(angles, Ref_P_H, color = "blue", zorder = 1, label = "H - Transmitted - Experimental ")
plt.title('Plot of Horizontally Polarized Reflected and Transmitted Power VS Angle of Incidence')
plt.xlabel('Angle (degrees)')
plt.ylabel('Power (μW)')
plt.legend()
plt.grid()
plt.show()


#plotting Vertically polarized Reflected and Transmitted VS angle
# plt.figure()
plot_V()
plt.scatter(angles, Trans_P_V, color = 'red')
plt.plot(angles, Trans_P_V, color = "red", zorder = 1, label = "V - Reflected - Experimental")
plt.scatter(angles, Ref_P_V, color = 'blue')
plt.plot(angles, Ref_P_V, color = "blue", zorder = 1, label = "H - Transmitted - Experimental ")
plt.title('Plot of Vertically Polarized Reflected and Transmitted Power VS Angle of Incidence')
plt.xlabel('Angle (degrees)')
plt.ylabel('Power (μW)')
plt.legend()
plt.grid()
plt.show()


#%%

min_index = np.argmin(Ref_P_V)
brewster_angle_exp = angles.iloc[min_index]
brewster_power_min = Ref_P_V.iloc[min_index]

print("Experimental Brewster angle =", brewster_angle_exp)

plt.figure()
plt.plot(angles, Ref_P_V, color='blue')
plt.scatter(brewster_angle_exp, brewster_power_min, color='red', label=f'Brewster angle = {brewster_angle_exp:.2f}°')
plt.axvline(brewster_angle_exp, color='red', linestyle='--')
plt.xlabel('Angle (degrees)')
plt.ylabel('Reflected p-polarized power (μW)')
plt.title('Experimental Brewster Angle')
plt.legend()
plt.grid()
plt.show()

