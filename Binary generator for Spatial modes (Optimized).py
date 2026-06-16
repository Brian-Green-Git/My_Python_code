# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 12:40:43 2026

@author: Photonics LAB


Optimized version — generates mode tables instantly even for 256+ modes.
"""

import numpy as np
import pandas as pd
import os
#%%
class Variables:     
    def __init__(self, max_index):
        self.max_index = max_index
        self.bin_arr = []
        self.SP_Modes = []
        self.index1 = []
        self.index2 = []
        self.save_path = r"C:\Users\Photonics LAB\Documents\Hybrid Optical comms experiment\Spatial mode and Binary conversion table\Conversion_table.xlsx"
#%%
def Calculate_binary_value(numBits, position):
    k = np.arange(numBits - 1, -1, -1)
    return np.mod(np.floor(position / (2**k)), 2).astype(int).tolist()

def generate_all_valid_pairs(max_index):
    """Generate ALL valid pairs for each family up to max_index.
    Returns dict: {family_name: [(i,k), ...]}"""
    
    pairs = {'HG': [], 'LG': [], 'SUPER HG': [], 'SUPER LG': []}
    
    # HG: all (n,m) with 0 ≤ n,m ≤ max_index, n+m > 0 (skip (0,0))
    # Include BOTH (n,m) and (m,n) since they look different on CCD (rotated)
    for n in range(max_index + 1):
        for m in range(max_index + 1):
            if n == 0 and m == 0:
                continue
            pairs['HG'].append((n, m))
    
    # LG: all (p,l) with 0 ≤ p ≤ max_index, 0 ≤ l ≤ max_index, skip (0,0)
    # Only non-negative l (intensity same for ±l)
    for p in range(max_index + 1):
        for l_val in range(max_index + 1):
            if p == 0 and l_val == 0:
                continue
            pairs['LG'].append((p, l_val))
    
    # SUPER HG: HG(n,m) + HG(m,n) with n < m (avoids duplicates)
    # Max index applies to both n and m
    for n in range(max_index + 1):
        for m in range(n + 1, max_index + 1):
            pairs['SUPER HG'].append((n, m))
    
    # SUPER LG: LG(p,+l) + LG(p,-l) with l > 0
    # Max index applies to both p and l
    for p in range(max_index + 1):
        for l_val in range(1, max_index + 1):
            pairs['SUPER LG'].append((p, l_val))
    
    return pairs

#%%
max_index = 8  # maximum order
total_modes = 128  # or however many you need

Var = Variables(max_index)

# Generate all valid pairs
all_pairs = generate_all_valid_pairs(max_index)

print("Available modes per family:")
for family in ['HG', 'LG', 'SUPER HG', 'SUPER LG']:
    print(f"  {family}: {len(all_pairs[family])} modes")
print(f"  Total: {sum(len(v) for v in all_pairs.values())}")

#%%
# Build the mode list with HG(0,0) first, then alternate across families
Var.SP_Modes.append('HG')
Var.index1.append(0)
Var.index2.append(0)

# Interleave families for even distribution
families = ['HG', 'LG', 'SUPER HG', 'SUPER LG']
family_indices = {f: 0 for f in families}

# Remove (0,0) from HG list since we added it manually
all_pairs['HG'] = [(n,m) for (n,m) in all_pairs['HG'] if not (n==0 and m==0)]

while len(Var.SP_Modes) < total_modes:
    added_any = False
    for family in families:
        if len(Var.SP_Modes) >= total_modes:
            break
        idx = family_indices[family]
        if idx < len(all_pairs[family]):
            n, m = all_pairs[family][idx]
            Var.SP_Modes.append(family)
            Var.index1.append(n)
            Var.index2.append(m)
            family_indices[family] += 1
            added_any = True
    if not added_any:
        print(f"Ran out of modes at {len(Var.SP_Modes)} total")
        break

#%%
df = pd.DataFrame()
df["Spatial Modes"] = Var.SP_Modes
df["Index 1"] = Var.index1
df["Index 2"] = Var.index2

numBits = int(np.ceil(np.log2(len(df))))
if 2**numBits < len(df):
    numBits += 1
Var.bin_arr = [Calculate_binary_value(numBits, i) for i in range(len(df))]
df["Binary Values"] = Var.bin_arr

#%%
os.makedirs(os.path.dirname(Var.save_path), exist_ok=True)
df.to_excel(Var.save_path, index=False)

print(f"\nGenerated {len(df)} modes with {numBits}-bit encoding")
