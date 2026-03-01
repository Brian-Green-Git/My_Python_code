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

#%% Fetching data
df = pd.read_csv(r"C:\Users\brian green\Desktop\Python\Python\Beam_profiling_results_01.csv")

#%% Measurement positions of scanning sensor

sensor_position = np.arange(0.02, 0.41, 0.02) # Positions are in meters

Beam_waist_vs_position_df = pd.DataFrame(sensor_position, columns = ["Position"])

#%% Classes

class IndependentClean:
    def __init__(self, df):
        # Dropping all the NAN values in the Dataframes 
      
        self.df1 = df[['Position_1', 'Intensity_1']].dropna()
        self.df2 = df[['Position_2', 'Intensity_2']].dropna()
        self.df3 = df[['Position_3', 'Intensity_3']].dropna()
        self.df4 = df[['Position_4', 'Intensity_4']].dropna()
        self.df5 = df[['Position_5', 'Intensity_5']].dropna()
        self.df6 = df[['Position_6', 'Intensity_6']].dropna()
        self.df7 = df[['Position_7', 'Intensity_7']].dropna()
        self.df8 = df[['Position_8', 'Intensity_8']].dropna()
        self.df9 = df[['Position_9', 'Intensity_9']].dropna()
        self.df10 = df[['Position_10', 'Intensity_10']].dropna()
        self.df11 = df[['Position_11', 'Intensity_11']].dropna()
        self.df12 = df[['Position_12', 'Intensity_12']].dropna()
        self.df13 = df[['Position_13', 'Intensity_13']].dropna()
        self.df14 = df[['Position_14', 'Intensity_14']].dropna()
        self.df15 = df[['Position_15', 'Intensity_15']].dropna()
        self.df16 = df[['Position_16', 'Intensity_16']].dropna()
        self.df17 = df[['Position_17', 'Intensity_17']].dropna()
        self.df18 = df[['Position_18', 'Intensity_18']].dropna()
        self.df19 = df[['Position_19', 'Intensity_19']].dropna()
        self.df20 = df[['Position_20', 'Intensity_20']].dropna()
        
class Recombine(IndependentClean):
    def __init__(self, df):
        super().__init__(df)

    def combined(self):
        # Reseting the indexes of each Dataframe
        
        df1 = self.df1.reset_index(drop=True)
        df2 = self.df2.reset_index(drop=True)
        df3 = self.df3.reset_index(drop=True)
        df4 = self.df4.reset_index(drop=True)
        df5 = self.df5.reset_index(drop=True)
        df6 = self.df6.reset_index(drop=True)
        df7 = self.df7.reset_index(drop=True)
        df8 = self.df8.reset_index(drop=True)
        df9 = self.df9.reset_index(drop=True)
        df10 = self.df10.reset_index(drop=True)
        df11 = self.df11.reset_index(drop=True)
        df12 = self.df12.reset_index(drop=True)
        df13 = self.df13.reset_index(drop=True)
        df14 = self.df14.reset_index(drop=True)
        df15 = self.df15.reset_index(drop=True)
        df16 = self.df16.reset_index(drop=True)
        df17 = self.df17.reset_index(drop=True)
        df18 = self.df18.reset_index(drop=True)
        df19 = self.df19.reset_index(drop=True)
        df20 = self.df20.reset_index(drop=True)

        # Recombining all the individual Dataframes into a single Dataframe
        combined_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, 
                                  df13, df14, df15, df16, df17, df18, df19, df20], axis=1)
        return combined_df

class Fitting_model:

    # Define the Gaussian model function
    def gaussian(self, x, amplitude, mean, sigma, offset):
        return amplitude * np.exp(-((x - mean)**2) / (2 * sigma**2)) + offset
    
    # Automated Initial Guess
    def guess(self, x, y):
        amplitude_guess = np.max(y) - np.min(y)
        mean_guess = x[np.argmax(y)]
        sigma_guess = np.sqrt(np.abs(np.sum(y * (x - mean_guess)**2) / np.sum(y)))
        offset_guess = np.min(y)
    
        return [amplitude_guess, mean_guess, sigma_guess, offset_guess]
        
#%% Filling nan values 
df = df.fillna(0) 

#%% Cleaning
df = df.drop_duplicates() 

# Filter out and Replace unwanted values with NaN
# Can edit the replace values to remove unwanted values from the Dataframe
# df = df.replace([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5], np.nan) 
df = df.replace([0], np.nan) 

# Dropping Nan values
cleaned = Recombine(df)

#%% Recombining Data cleaned data 
final_df = cleaned.combined()

#%% Plotting the cleaned data 

# Plotting each incremented graph
# for i in range (1, 21, 4): 
#     plt.figure()
#     plt.plot(final_df["Position_"+ str(i)], final_df["Intensity_"+ str(i)], color = "red", linestyle='--')
#     plt.scatter(final_df["Position_"+ str(i)], final_df["Intensity_"+ str(i)], color = "cyan", zorder = 2)
#     plt.xlabel("Position_" + str(i))
#     plt.ylabel("Intensity_"+ str(i))
#     plt.title("Intensity_"+ str(i) + " VS Position_" + str(i))
#     plt.show()
    
#%% Fitting the data and extracting the beam waist

beam_waist_list = []

def beam_waist(sigma):
    beam_waist = 2 * sigma
    beam_waist_list.append(beam_waist)  
    
    # print("Beam waist (1/e^2 radius):", beam_waist    

for i in range(1, 21, 1):
    
    x = final_df["Position_" + str(i)]
    y = final_df["Intensity_" + str(i)]
    
    x = x.dropna()
    y = y.dropna()
    
    # Fitting model class object
    Fitting = Fitting_model()
    
    # Fit the curve
    popt, pcov = curve_fit(Fitting.gaussian, x, y, p0=Fitting.guess(x, y))
    
    amplitude, mean, sigma, offset = popt
 
    # Create a sorted x-axis for a smooth, single line
    x_smooth = np.linspace(np.min(x), np.max(x), 500) 
    # x_smooth = np.linspace(mean - 4*sigma, mean + 4*sigma, 500) # smooth tail on both sides
    t = Fitting.gaussian(x_smooth, *popt)
    
    beam_waist(sigma)
    
    # equation = f"y_{i} = {amplitude:.10f} * exp(-(x - {mean:.10f})^2 / (2 * {sigma:.10f}^2))"
    # print(f"\nPosition {i} Equation: {equation}\n\n")
       
    # plt.figure()
    # plt.legend()
    # plt.xlabel("Position_" + str(i))
    # plt.ylabel("Intensity_" + str(i))
    # # Plot the results
    # plt.scatter(x, y, label='Data', color='black')
    # # plt.plot(x, y, color = "black", zorder = 2 )
    
    # plt.plot(x, y, color = "black", zorder = 2)
    # # Plot the fit
    # plt.plot(x_smooth, t, label='Gaussian Fit', color='red', lw=2)
    # plt.show()
    
#%%

Beam_waist_vs_position_df["Waist"] = beam_waist_list

Beam_waist_vs_position_df["Waist^2"] = Beam_waist_vs_position_df["Waist"]**2

#%% Plotting Position VS beam waist

# plt.figure()
# plt.title("Position VS Waist")
# plt.xlabel("Positon of sensor")
# plt.ylabel("Beam waist")
# plt.scatter(Beam_waist_vs_position_df["Position"], Beam_waist_vs_position_df["Waist"], color = "black")
# plt.plot(Beam_waist_vs_position_df["Position"], Beam_waist_vs_position_df["Waist"], color = "black", zorder = 2)
# plt.show()

#%% Plotting Position VS Beam waist squared

# plt.figure()
# plt.title("Position VS Waist Squared")
# plt.xlabel("Positon of sensor")
# plt.ylabel("Beam waist squared")
# plt.scatter(Beam_waist_vs_position_df["Position"], Beam_waist_vs_position_df["Waist^2"], color = "blue")
# plt.plot(Beam_waist_vs_position_df["Position"], Beam_waist_vs_position_df["Waist^2"], color = "blue", zorder = 2)
# plt.show()

#%% Fitting the quadratic plot of position vs beam waist squared

x = Beam_waist_vs_position_df["Position"]
y = Beam_waist_vs_position_df["Waist^2"]

# Fit a 2nd-degree polynomial (a=coef[0], b=coef[1], c=coef[2])
coef = np.polyfit(x, y, 2)

a, b, c = coef
print(f"\n\nThe equation of Position VS Beam Waist Squared is: \ny = {a}x² + {b}x + {c}")

# Create a function based on the coefficients
p_function = np.poly1d(coef)

# Now you can plug in any X to get the predicted Y
y_pred = p_function(x) 

# Generate smooth X values for a pretty curve
x_smooth = np.linspace(x.min(), x.max(), 100)
y_smooth = p_function(x_smooth)

plt.figure()
plt.title("Position VS Waist Squared")
plt.xlabel("Positon of sensor")
plt.ylabel("Beam waist squared")
plt.scatter(x, y, label="Data Points", color="blue")
plt.plot(x, y, color = "blue", zorder = 2)
plt.plot(x_smooth, y_smooth, label="Parabolic Fit", color="red")
plt.legend()
plt.show()

#%%

pi = 3.14159
M_sqr = float()
Wavelength = 633E-9
W_o = float()
Z_o = float()

#%%

Z_o = b/(-2 * a) 

print(f"\n\nZ_0 value is: {Z_o} meters")

W_o = np.sqrt(((c) - ((a)*(Z_o)**2)))

print(f"W_o is : {W_o}")

val = np.sqrt(a)

M_sqr = val * (pi) * (W_o)

M_sqr = M_sqr / Wavelength

print(f"M_Squared value is: {M_sqr}")

ax = plt.gca()
ax.text(0.35, 0.95,
        f"M² = {M_sqr:.2f}\n"
        f"w₀ = {W_o:.3e} m\n"
        f"z₀ = {Z_o:.3f} m",
        transform=ax.transAxes,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8))
