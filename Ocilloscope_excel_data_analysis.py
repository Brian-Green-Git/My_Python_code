# -*- coding: utf-8 -*-
"""
Created on Tue May 12 11:51:40 2026

@author: Photonics LAB
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks 

#%%

file = r"C:\Users\Photonics LAB\Documents\Hybrid Optical comms experiment\Ocilloscope tests\test_vals_12_05_26_xlsx_file.xlsx"

df = pd.read_excel(file)

df.shape

#%% Filtering 

df['math'] = df['math'].str.replace(r'[!@#$,]', '', regex=True) # replaces the , in the data 

df['math'] = pd.to_numeric(df['math'], errors='coerce') # converts the str into int

Noise_Filter_val = 5 # intensity of noise to be filtered out

for col in df.columns:
    for values in df[col]:
            df = df.replace(values, (values-1))
               
for col in df.columns:
    for values in df[col]:
        if (values < Noise_Filter_val and values > 0) and (not(values > Noise_Filter_val)) == True:
            df = df.replace(values, 0)
        if (values < 0) and (not(values < -Noise_Filter_val)) == True:
            df = df.replace(values, 0)
                     
#%% plotting

length_of_df = df.shape[0]

x_vals = np.arange(0, length_of_df, 1) # start, stop, step
y_vals = df['math']

plt.figure()
plt.xlabel('time')
plt.ylabel('intensity')
plt.plot(x_vals, y_vals, color = 'black', linewidth = 2, label = 'Cleaned Data')
#%% Getting the peaks 

Amplitude = 15
peaks, _ = find_peaks(y_vals, height = Amplitude) #adjust height thresholding 
troughs, _ = find_peaks(-y_vals, height = Amplitude)# detect the troughs by inverting the signal

plt.scatter(troughs, y_vals[troughs], color = 'blue', zorder = 1, label = 'Troughs')
plt.scatter(peaks, y_vals[peaks], color = 'green', zorder = 2, label = 'Peaks')
plt.show()

print(f"Peaks:: {y_vals[peaks]}")
print(f"Troughs:: {y_vals[troughs]}")

#%% Using np.fft to do an fft

Number_of_vals = len(y_vals)
fft_vals = np.fft.fftn(y_vals)
Frequencies = np.fft.fftfreq(Number_of_vals)

N = 20 # take the n strongest Frequencies 
indices = np.argsort(np.abs(fft_vals))[-N:]

ind = np.argsort(np.abs(Frequencies))[-N:]

y_vals_reconstructed = np.zeros(Number_of_vals, dtype = complex)
y_vals_reconstructed[indices] = fft_vals[indices]
y_vals_final = np.fft.ifft(y_vals_reconstructed).real

Frequencies = np.abs(Frequencies)

Frequencies_reconstructed = np.zeros(Number_of_vals, dtype = complex)
Frequencies_reconstructed[ind] = Frequencies[ind]
Frequencies_final = np.fft.ifft(y_vals_reconstructed).real

Frequencies = Frequencies * 1e2

#%% Ploting fft 

# plt.figure()
# plt.xlabel('time')
# plt.ylabel('intensity')
plt.plot(x_vals, y_vals_final, label = 'FFt Reconstruction', color = 'red', zorder = 3)
plt.plot(x_vals, Frequencies, label = 'Frequencies', color = 'yellow', zorder = 4)
plt.legend()
plt.grid(visible = True)
plt.show()

#%% Creating a dataframe with the detected peaks and troughs

# df = pd.DataFrame({"Peak_Postions" : y_vals[peaks].index, 
#                    "Detected_Peaks": y_vals[peaks], 
#                    "Trough_Postions": y_vals[troughs].index, 
#                    "Detected_Troughs": y_vals[troughs]})

df = pd.DataFrame({"Detected_Peaks": y_vals[peaks],
                  "Detected_Troughs": y_vals[troughs]})

# z = np.fft.f



# plt.figure()
# # plt.xlabel('time')
# # plt.ylabel('intensity')
# plt.plot(x_vals, Frequencies, label = 'Frequencies', color = 'yellow')
# plt.legend()
# plt.show()



















