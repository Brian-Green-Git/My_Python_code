# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:06:08 2026

@author: Photonics LAB
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 15:36:21 2026

@author: brian green
"""

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re
import os

#%% ================= USER SETTINGS =================

# File path
# FILE_PATH = r"C:\Users\Photonics LAB\Documents\Beam Profiling\Beam_profiling_data_09_04_26_001.xlsx"
FILE_PATH = r"D:\thuso beam profile_e.xlsx"

# Sensor positions along propagation axis (z) in meters
# IMPORTANT: This must match your experiment
SENSOR_POSITIONS = np.arange(0.01, 1.16, 0.02)

# Unit conversion for transverse beam-profile positions
# Example:
#   mm -> m : 1e-3
#   um -> m : 1e-6
#   m  -> m : 1
POSITION_UNIT_TO_M = 1e-3

# Laser wavelength in meters
WAVELENGTH = 633e-9

# Fit quality settings
# What each threshold is really doing

MAX_RELATIVE_ERROR = 0.9
# Rejects fits that are numerically uncertain.
# 0.3 for strict filtering
# 0.5 for moderate filtering
# 1.0 for loose filtering

MIN_WAIST_M = 1e-7
# Rejects absurdly tiny fitted beams, usually caused by fitting noise spikes.

MAX_WAIST_M = 0.1e-1
# MAX_WAIST_M = 0.1
# Rejects absurdly broad fitted beams, usually caused by flat or badly truncated data.

# Replace zeros with NaN
REPLACE_ZERO_WITH_NAN = True

#%% Fetching data
df = pd.read_excel(FILE_PATH)
# df = pd.read_csv(FILE_PATH)

#%% Classes

class IndependentClean:
    def __init__(self, df):
        self.df = df

        self.run_numbers = []
        self.position_columns = {}
        self.intensity_columns = {}

        # Automatically detect columns for each run
        for col in df.columns:
            col_text = str(col)
            match = re.search(r'Run\s*#?\s*(\d+)', col_text)
            # match = re.search(r'_(\d+)', col_text)
                              # Position (mm) Run #4

            if match:
                run_num = int(match.group(1))
                col_lower = col_text.lower()

                if "position" in col_lower:
                    self.position_columns[run_num] = col_text

                if "intensity" in col_lower:
                    self.intensity_columns[run_num] = col_text

        # Keep only runs that have both position and intensity columns
        common_runs = sorted(set(self.position_columns.keys()).intersection(set(self.intensity_columns.keys())))
        self.run_numbers = common_runs

        # Build cleaned run data
        self.run_data = {}

        for run_num in self.run_numbers:
            pos_col = self.position_columns[run_num]
            int_col = self.intensity_columns[run_num]

            pair_df = df[[pos_col, int_col]].dropna()
            self.run_data[run_num] = pair_df


class Recombine(IndependentClean):
    def __init__(self, df):
        super().__init__(df)

    def combined(self):
        combined_list = []

        for run_num in self.run_numbers:
            pair_df = self.run_data[run_num].reset_index(drop=True).copy()

            pos_col = self.position_columns[run_num]

            # Convert transverse position to meters
            pair_df[pos_col] = pair_df[pos_col] * POSITION_UNIT_TO_M

            combined_list.append(pair_df)

        combined_df = pd.concat(combined_list, axis=1)
        return combined_df

class Fitting_model:

    # Define the Gaussian model function
    def gaussian(self, x, amplitude, mean, sigma, offset):
        return amplitude * np.exp(-((x - mean)**2) / (2 * sigma**2)) + offset

    # Automated Initial Guess
    def guess(self, x, y):
        amplitude_guess = np.max(y) - np.min(y)
        mean_guess = x[np.argmax(y)]

        y_shift = y - np.min(y)

        if np.sum(y_shift) == 0:
            sigma_guess = (np.max(x) - np.min(x)) / 4
        else:
            sigma_guess = np.sqrt(np.abs(np.sum(y_shift * (x - mean_guess)**2) / np.sum(y_shift)))

        if sigma_guess == 0:
            sigma_guess = (np.max(x) - np.min(x)) / 4

        offset_guess = np.min(y)

        return [amplitude_guess, mean_guess, sigma_guess, offset_guess]
#%% Cleaning

df = df.fillna(0)
df = df.drop_duplicates()

if REPLACE_ZERO_WITH_NAN:
    df = df.replace([0], np.nan)

# for col in df.columns:
#     for value in df[col]:
#         if value < 0:
#             df = df.replace(value, np.nan)
            
#%% Dropping Nan values and recombining data
cleaned = Recombine(df)
final_df = cleaned.combined()

run_numbers = cleaned.run_numbers

print(f"Detected run numbers: {run_numbers}")
print("\n\n")

if len(SENSOR_POSITIONS) < len(run_numbers):
    raise ValueError("Not enough SENSOR_POSITIONS were provided for the number of detected runs.")
    print("\n\n")

#%% Plotting the cleaned data

# # Uncomment if needed
# for run_num in range (1, len(run_numbers), 5): 
#     plt.figure()
#     pos_col = cleaned.position_columns[run_num]
#     int_col = cleaned.intensity_columns[run_num]
#     plt.plot(final_df[pos_col], final_df[int_col], color="red", linestyle="--")
#     plt.scatter(final_df[pos_col], final_df[int_col], color="cyan", zorder=2)
#     plt.xlabel(f"Position (m) Run #{run_num}")
#     plt.ylabel(f"Light Intensity Run #{run_num}")
#     plt.title(f"Light Intensity Run #{run_num} VS Position Run #{run_num}")
#     plt.show()

#%% Fitting the data and extracting the beam waist

beam_waist_list = []
accepted_positions = []
accepted_run_numbers = []
rejected_runs = []

def beam_waist(sigma):
    beam_waist = 2 * abs(sigma)
    beam_waist_list.append(beam_waist)

for index, run_num in enumerate(run_numbers):

    pos_col = cleaned.position_columns[run_num]
    int_col = cleaned.intensity_columns[run_num]

    x = final_df[pos_col].dropna().to_numpy()
    y = final_df[int_col].dropna().to_numpy()

    if len(x) < 4 or len(y) < 4:
        print(f"Run {run_num} rejected: not enough data points")
        continue

    # Fitting model class object
    Fitting = Fitting_model()

    try:
        # Fit the curve
        popt, pcov = curve_fit(
            Fitting.gaussian,
            x,
            y,
            p0=Fitting.guess(x, y),
            maxfev=10000
        )
    except Exception as error:
        print(f"Run {run_num} rejected: fit failed ({error})")
        rejected_runs.append((run_num, "fit failed"))
        continue

    uncertainty = np.sqrt(np.diag(pcov))
    relative_error = np.full(len(popt), np.inf)

    for j in range(len(popt)):
        if abs(popt[j]) > 1e-15:
            relative_error[j] = uncertainty[j] / abs(popt[j])


    #Checking the relative error across all the data points
    print(f"Run {run_num}: relative errors = {relative_error}")
    
    
    # Filter by fit quality
    if np.any(relative_error > MAX_RELATIVE_ERROR):
        print(f"Run {run_num} rejected: high relative uncertainty")
        rejected_runs.append((run_num, "high uncertainty"))
        print("\n")
        continue
        
    amplitude, mean, sigma, offset = popt

    x_smooth = np.linspace(np.min(x), np.max(x), 500)
    t = Fitting.gaussian(x_smooth, *popt)

    current_waist = 2 * abs(sigma)
    
    print(f"Run {run_num}: waist = {current_waist:.3e} m")

    print(f"Run {run_num}: sigma = {sigma:.3e} m, waist = {current_waist:.3e} m, mean = {mean:.3e} m")

    # Throw away bad runs based on physical waist range
    if MIN_WAIST_M < current_waist < MAX_WAIST_M:
        beam_waist(sigma)
        accepted_positions.append(SENSOR_POSITIONS[index])
        accepted_run_numbers.append(run_num)
    else:
        print(f"Run {run_num} rejected: waist = {current_waist:.3e} m")
        rejected_runs.append((run_num, f"bad waist ({current_waist:.3e} m)"))

    # # Uncomment if needed
    # plt.figure()
    # plt.xlabel(f"Position (m) Run #{run_num}")
    # plt.ylabel(f"Light Intensity Run #{run_num}")
    # plt.scatter(x, y, label="Data", color="black")
    # plt.plot(x, y, color="black", zorder=2)
    # plt.plot(x_smooth, t, label="Gaussian Fit", color="red", lw=2)
    # plt.legend()
    # plt.show()
    
    print("\n")
#%% Accepted waist dataframe

print("\n\n")

if len(beam_waist_list) < 3:
    raise ValueError("Not enough accepted beam waist points to fit a quadratic propagation curve.")

Beam_waist_vs_position_df = pd.DataFrame({
    "Run": accepted_run_numbers,
    "Position": accepted_positions,
    "Waist": beam_waist_list
})

Beam_waist_vs_position_df["Waist^2"] = Beam_waist_vs_position_df["Waist"]**2

print("\nAccepted runs:")
print(Beam_waist_vs_position_df)

# # create a path to save the beam wasit parameters 
# save_path = r"C:\Users\Photonics LAB\Documents\Beam Profiling\Beam profling lerato\Analyzed Beam Waist Data (Accepted Runs only).xlsx"

# try:
#     # Make save location
#     os.makedirs(os.path.dirname(save_path), exist_ok = True)
    
#     # Save Data to Excel
#     Beam_waist_vs_position_df.to_excel(save_path, index = True)  # index = False to avoid writing row numbers
#     print(f"File saved successfully at: {save_path}")

# except PermissionError:
#     print("Permission denied: Please check if the file is open or if you have write access.")
# except FileNotFoundError:
#     print("Invalid path: Please check the directory.")
# except Exception as e:
#     print(f"An error occurred: {e}")


print("\nRejected runs:")
if len(rejected_runs) == 0:
    print("None")
else:
    for run, reason in rejected_runs:
        print(f"Run {run}: {reason}")
#%% Plotting Position VS beam waist

# Uncomment if needed
# plt.figure()
# plt.title("Position VS Waist")
# plt.xlabel("Position of sensor (m)")
# plt.ylabel("Beam waist (m)")
# plt.scatter(Beam_waist_vs_position_df["Position"], Beam_waist_vs_position_df["Waist"], color="black")
# plt.plot(Beam_waist_vs_position_df["Position"], Beam_waist_vs_position_df["Waist"], color="black", zorder=2)
# plt.show()

#%% Fitting the quadratic plot of position vs beam waist squared

# Beam_waist_vs_position_df = pd.read_excel(r"D:\Analyzed Beam Waist Data (Accepted Runs only)revised.xlsx")

x = Beam_waist_vs_position_df["Position"].to_numpy()
y = Beam_waist_vs_position_df["Waist^2"].to_numpy()

if np.any(np.isnan(x)) or np.any(np.isnan(y)):
    raise ValueError("NaN values found in propagation fit data.")

if len(x) < 3:
    raise ValueError("Not enough accepted beam waist points to fit a quadratic.")

# Fit a 2nd-degree polynomial
coef = np.polyfit(x, y, 2)

a, b, c = coef
print(f"\nThe equation of Position VS Beam Waist Squared is:\ny = {a}x² + {b}x + {c}")

# Create a function based on the coefficients
p_function = np.poly1d(coef)

# Predicted Y values
y_pred = p_function(x)


plt.figure()
plt.scatter(x, y, color = 'blue', label = 'Points')
plt.plot(x, y, color = 'black', zorder = 1)
plt.legend()
plt.show()


# Generate smooth X values for a pretty curve
x_smooth = np.linspace(x.min(), x.max(), 100)
y_smooth = p_function(x_smooth)
#%% M-squared calculation

pi = np.pi

Z_o = -b / (2 * a)

if a <= 0:
    raise ValueError("Quadratic coefficient a must be positive for a physical beam propagation fit.")

w0_sq = c - a * Z_o**2

# w0_sq = np.abs(w0_sq)

if w0_sq <= 0:
    raise ValueError("Computed w0^2 is non-positive. Fit is not physically valid.")

W_o = np.sqrt(w0_sq)
M_sqr = (pi * W_o * np.sqrt(a)) / WAVELENGTH

print(f"\nZ_0 value is: {Z_o} meters")
print(f"W_o is: {W_o} meters")
print(f"M_Squared value is: {M_sqr}")
#%% Final plot

plt.figure()
plt.title("Position VS Beam Waist Squared")
plt.xlabel("Position of sensor (m)")
plt.ylabel("Beam waist squared (m$^2$)")
plt.scatter(x, y, label="Data Points", color="blue")
plt.plot(x, y, color="blue", zorder=2)
plt.plot(x_smooth, y_smooth, label="Parabolic Fit", color="red")

ax = plt.gca()
ax.text(0.35, 0.95,
        f"M² = {M_sqr:.2f}\n"
        f"w₀ = {W_o:.3e} m\n"
        f"z₀ = {Z_o:.3f} m",
        transform=ax.transAxes,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8))

plt.legend()
plt.show()