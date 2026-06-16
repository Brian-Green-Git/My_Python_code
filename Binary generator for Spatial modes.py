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
            
            # =========================================================
            # HG MODES: HG(n,m)
            # Intensity = rectangular array of (n+1)×(m+1) lobes
            # HG(n,m) and HG(m,n) are 90° rotations — DISTINCT on CCD
            # HG(0,0) is the fundamental Gaussian — already added
            # =========================================================
            if mode_family == 'HG':
                if i == 0 and k == 0:
                    skip = True
            
            # =========================================================
            # LG MODES: LG(p,l)
            # Intensity = p+1 concentric rings with central null for l≠0
            # LG(p,+l) and LG(p,-l) have SAME intensity — indistinguishable on CCD
            # So we only use NON-NEGATIVE l
            # LG(0,0) is Gaussian — already covered by HG(0,0)
            # =========================================================
            elif mode_family == 'LG':
                # Skip (0,0) — same as HG(0,0)
                if i == 0 and k == 0:
                    skip = True
                # Skip if p=0 and l>0 — these are pure vortices,
                # but LG(0,l) intensity differs from HG(0,l) intensity,
                # so they ARE distinct. Keep them.
            
            # =========================================================
            # SUPER HG: HG(n,m) + HG(m,n)  with n ≠ m
            # Intensity = interference of two rotated HG modes
            # If n=m: HG(n,n)+HG(n,n) = 2×HG(n,n) — same intensity as HG(n,n)
            # If n=0 or m=0: HG(0,m)+HG(m,0) looks like a rotated single HG
            #   Actually HG(0,m) has m+1 vertical lobes,
            #   HG(m,0) has m+1 horizontal lobes,
            #   their sum has a cross pattern — DISTINCT from single HG!
            #   But HG(0,1)+HG(1,0) = HG(1,0)+HG(0,1) by symmetry,
            #   so we need n < m to avoid duplicates.
            # =========================================================
            elif mode_family == 'SUPER HG':
                # Must have n < m to avoid duplicate pairs
                if i >= k:
                    skip = True
                # Skip if either is zero? HG(0,2)+HG(2,0) is cross-shaped,
                # distinct from HG(2,0) or HG(0,2) alone. KEEP these.
            
            # =========================================================
            # SUPER LG: LG(p,+l) + LG(p,-l)  with l > 0
            # Intensity = petal pattern with 2l petals and p+1 rings
            # If l=0: LG(p,0)+LG(p,0) = 2×LG(p,0) — same as single LG(p,0)
            # If p=0: petal pattern — distinct from single LG(0,l) (doughnut)
            #   Actually LG(0,+l)+LG(0,-l) produces 2l petals,
            #   while LG(0,l) is a doughnut — DISTINCT!
            #   So we KEEP p=0, l>0 for SUPER LG.
            # =========================================================
            elif mode_family == 'SUPER LG':
                # Must have l > 0 (otherwise no petal pattern)
                if k == 0:
                    skip = True
                # Must have p ≥ 0 (p=0 is allowed — gives 2l petals)
                # i is p, k is l — no other restrictions needed
                # LG(p,+l)+LG(p,-l) is symmetric in ±l, so l is always positive
            
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
