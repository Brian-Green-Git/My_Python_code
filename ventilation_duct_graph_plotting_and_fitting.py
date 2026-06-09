# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 12:05:30 2026

@author: Brian Green
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#%%Experimental data
val1 = (0.029+0.030)/2
val2 = (0.026+0.027)/2

values = [0.033, val1, val2, 0.023, 0.021, 0.016, 0.013, 0.010]

vals_arr = np.array(values) # psi
x_arr = np.array([0, 2.5, 5, 7.5, 10, 15, 20, 25]) # centimeters 

#%% Fitting fuctions
def exponential_func(x, A, B):
    return A * np.exp(B * x)

def linear_func(x, m, c):
    return m*x + c

#%% Exponential fitting
stop_exp = 40
x_vals = np.arange(0, stop_exp, 2.5)
x = x_arr
y = vals_arr
popt, pcov = curve_fit(exponential_func, x, y, p0=[1, 1])
A_opt, B_opt = popt
print(f"Exponential Optimized Parameters -> A: {A_opt:.5f}, B: {B_opt:.5f}")
y_vals = exponential_func(x_vals, A_opt, B_opt)

#%%Plotting experimental data
plt.figure()
plt.title('Velocity Pressure VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Velocity Pressure (psi)')
plt.scatter(x_arr, vals_arr, color = 'red')
plt.plot(x_arr, vals_arr, zorder = 1, color = 'red', label = 'Experimental results')
plt.grid()
plt.legend()
plt.show()

# %% Goodness of Fit Calculation
# 1. Calculate the predicted y-values for your original x data points
y_pred = exponential_func(x, A_opt, B_opt)

# 2. Calculate the residuals (differences between experimental and predicted data)
residuals = y - y_pred

# 3. Calculate Residual Sum of Squares (SS_res) and Total Sum of Squares (SS_tot)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)

# 4. Calculate R-squared
r_squared = 1 - (ss_res / ss_tot)

print(f"Residual Sum of Squares (SS_res): {ss_res:.8f}")
print(f"R-squared value (R²): {r_squared:.4f}")
#%%Plotting experimental data and exponential fit
plt.figure()
plt.title('Velocity Pressure VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Velocity Pressure (psi)')
plt.xticks(np.arange(0, stop_exp, 5))
plt.yticks(np.arange(0, 0.035, 0.002))
plt.scatter(x_arr, vals_arr, color = 'red')
plt.plot(x_arr, vals_arr, zorder = 2, color = 'red', label = 'Experimental results')
plt.plot(x_vals, y_vals, color = 'black', zorder = 3, label = 'Theoretical predictive exponential fit')
# Coordinates (40, 0.025) place the box in a clear, empty space on your chart
text_str = f'$R^2 = {r_squared:.4f}$'
plt.text(30, 0.028, text_str, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
plt.grid()
plt.legend()
plt.show()

#%%Linear fitting
stop_lin = 100
x_vals = np.arange(0, stop_lin, 5)
popt, pcov = curve_fit(linear_func, x, y, p0=[1, 1])
A_opt, B_opt = popt
print(f"Linear Optimized Parameters -> A: {A_opt:.5f}, B: {B_opt:.5f}")
y_vals = linear_func(x_vals, A_opt, B_opt)

# %% Goodness of Fit Calculation
# 1. Calculate the predicted y-values for your original x data points
y_pred = linear_func(x, A_opt, B_opt)

# 2. Calculate the residuals (differences between experimental and predicted data)
residuals = y - y_pred

# 3. Calculate Residual Sum of Squares (SS_res) and Total Sum of Squares (SS_tot)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)

# 4. Calculate R-squared
r_squared = 1 - (ss_res / ss_tot)

print(f"Residual Sum of Squares (SS_res): {ss_res:.8f}")
print(f"R-squared value (R²): {r_squared:.4f}")
#%%Plotting experiemtnal data and linear fit
plt.figure()
plt.title('Velocity Pressure VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Velocity Pressure (psi)')
plt.xticks(np.arange(0, stop_lin, 5))
plt.yticks(np.arange(-1, 0.035, 0.005))
plt.scatter(x_arr, vals_arr, color = 'red')
plt.plot(x_arr, vals_arr, zorder = 2, color = 'red', label = 'Experimental results')
plt.plot(x_vals, y_vals, color = 'black', zorder = 3, label = 'Theoretical predictive linear fit')
text_str = f'$R^2 = {r_squared:.4f}$'
plt.text(75, 0.017, text_str, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
plt.grid()
plt.legend()
plt.show()

#%% Calculating Air velocity From Bernoulli
def velocity_func(x):
    return np.sqrt((2*(x))/1.2)

values_Pascals = vals_arr * 6894.76 # Pascals

velocity_values = velocity_func(values_Pascals) # m/s

velocity_values = velocity_values * 100

#%%Plotting velocity vs position
plt.figure()
plt.title('Velocity of air VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Velocity of air (cm/s)')
plt.xticks(np.arange(0, 30, 2.5))
plt.yticks(np.arange(1000, 2000, 50))
plt.scatter(x_arr, velocity_values, color = 'red')
plt.plot(x_arr, velocity_values, zorder = 2, color = 'red', label = 'Experimental results')
plt.grid()
plt.legend()
plt.show()

#%% Fitting velocity to exponential fit
stop_vel = 100
x_vals = np.arange(0, stop_vel, 2.5)
popt, pcov = curve_fit(exponential_func, x, velocity_values, p0=[1, 1])
A_opt, B_opt = popt
exp_velocity_vals = exponential_func(x_vals, A_opt, B_opt)
print(f"Exponential velocity decay Optimized Parameters -> A: {A_opt:.5f}, B: {B_opt:.5f}")

#%%Plotting exponential fit of velocity vs position
plt.figure()
plt.title('Velocity of air VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Velocity of air (cm/s)')
plt.xticks(np.arange(0, stop_vel, 5))
plt.yticks(np.arange(100, 2000, 100))
plt.scatter(x_arr, velocity_values, color = 'red')
plt.plot(x_arr, velocity_values, zorder = 2, color = 'red', label = 'Experimental Velocity results')
plt.plot(x_vals, exp_velocity_vals, zorder = 3, color = 'black', label = 'Theoretical Velocity exponential fit')
plt.grid()
plt.legend()
plt.show()

#%% experimental

x_exp = np.array([0, 2.5, 5, 7.5, 10])
y_exp = np.array([90, 57, 25, 13, 7])

plt.figure()
plt.title('Expected velocity Percentage of air VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Expected velocity Percentage of air (%)')
plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.arange(0, 101, 10))

# Plot the points and line
plt.scatter(x_exp, y_exp, color = 'red')
plt.plot(x_exp, y_exp, zorder = 2, color = 'red', label = 'Theoretical expected percentage of air velocity')

for x_val, y_val in zip(x_exp, y_exp):
    label = f"{y_val}%"
    plt.annotate(
        label,                      # The text to display
        (x_val, y_val),             # Point coordinate to label
        textcoords="offset points", # Style text relative to the point
        xytext=(0, 10),             # Shift text 10 points vertically above point
        ha='center',                # Centered horizontally over point
        fontsize=9                 # Text font size
    )

plt.grid()
plt.legend()
plt.show()
#%% Plotting Experiment Vs Theory

x_exp = np.array([0, 2.5, 5, 7.5, 10])
y_ex = np.array([0.9, 0.57, 0.25, 0.13, 0.07])

y_exp = velocity_values[:5] * y_ex

velocity_values = velocity_values[:5]
x_arr = x_arr[:5]

plt.figure()
plt.title('Velocity of air VS Hood position from Duct')
plt.xlabel('Position of Hood from Duct (cm)')
plt.ylabel('Velocity of air (cm/s)')
plt.scatter(x_exp, y_exp, color = 'blue')
plt.plot(x_exp, y_exp, zorder = 2, color = 'blue', label = 'Theoretical expected air Velocity')
plt.scatter(x_arr, velocity_values, color = 'red')
plt.plot(x_arr, velocity_values, zorder = 3, color = 'red', label = 'Experimental air Velocity results')
plt.grid()
plt.legend()
plt.show()



