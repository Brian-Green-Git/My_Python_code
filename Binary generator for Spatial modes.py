# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:03:37 2026

@author: Photonics LAB

"""
import numpy as np
import pandas as pd
import os

#%%
class Variables:     
    def __init__(self, nummodes, modes):
        self.slots_per_family = int(np.ceil((nummodes - 1) / len(modes)))
        self.bin_arr = []
        self.SP_Modes = []
        self.index1 = []
        self.index2 = []
        self.grid_width = 8
        self.save_path = r"C:\Users\Photonics LAB\Documents\Hybrid Optical comms experiment\Spatial mode and Binary conversion table\Conversion_table.xlsx"
    
#%%
def Calculate_binary_value(num, position):
    numBits = int(np.log2(num))
    k = np.arange(numBits - 1, -1, -1)
    binaryValues = np.mod(np.floor(position / (2**k)), 2)
    return binaryValues

def Generate_modes(SP_Modes, index1, index2, grid_width, slots_per_family, numModes, Modes):
    family_counters = {mode: 0 for mode in Modes}
    
    for mode_family in Modes:
        local_idx = 0
        
        while family_counters[mode_family] < slots_per_family:
            if len(SP_Modes) >= numModes:
                break
            
            i = local_idx // grid_width  # index1
            k = local_idx % grid_width   # index2
            
            skip = False

            if mode_family == 'HG':
                if i == 0 and k == 0:
                    skip = True
            elif mode_family == 'LG':
                # Skip (0,0) — same as HG(0,0)
                if i == 0 and k == 0:
                    skip = True
            # =========================================================
            elif mode_family == 'SUPER HG':
                # Must have n < m to avoid duplicate pairs
                if i >= k:
                    skip = True
            # =========================================================
            elif mode_family == 'SUPER LG':
                # Must have l > 0 (otherwise no petal pattern)
                if k == 0:
                    skip = True
            
            if not skip:
                SP_Modes.append(mode_family)
                index1.append(i)
                index2.append(k)
                family_counters[mode_family] += 1
            
            local_idx += 1
    
    return SP_Modes, index1, index2
 
def Generate_binary(bin_arr, numModes, length):  
    for i in range(0, length):
        bin_arr.append(Calculate_binary_value(numModes, i))
    return bin_arr

#%%
numModes = 128
Modes = ['HG', 'LG', 'SUPER HG', 'SUPER LG']

Var = Variables(numModes, Modes)

# Start with HG(0,0) as the fundamental Gaussian
Var.SP_Modes.append('HG')
Var.index1.append(0)
Var.index2.append(0)

#%%
df = pd.DataFrame()

Var.SP_Modes, Var.index1, Var.index2 = Generate_modes(
    Var.SP_Modes, Var.index1, Var.index2, 
    Var.grid_width, 
    Var.slots_per_family, numModes, Modes
)

df["Spatial Modes"] = Var.SP_Modes
df["Index 1"] = Var.index1
df["Index 2"] = Var.index2
df["Binary Values"] = Generate_binary(Var.bin_arr, numModes, df.shape[0])  

#%%
os.makedirs(os.path.dirname(Var.save_path), exist_ok=True)
df.to_excel(Var.save_path, index=False)
