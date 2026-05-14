import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Load your experimental file
# -----------------------
df = pd.read_excel(r"C:\Users\Photonics LAB\Documents\Experimental results\Brewster experiment\Brewster_Data.xlsx")

angles_deg = df["Angle"].to_numpy(dtype=float)
Ref_H = df["Reflected_power_H_microW"].to_numpy(dtype=float)
Trans_H = df["Transmitted_power_H_microW"].to_numpy(dtype=float)
Ref_V = df["Reflected_power_V_microW"].to_numpy(dtype=float)
Trans_V = df["Transmitted_power_V_microW"].to_numpy(dtype=float)

# Incident power at sample (µW). Forward-fill if recorded once.
P_in_uW = (df["Power_Io_mW"].ffill().to_numpy(dtype=float) * 1e3)

# -----------------------
# Fresnel (single interface)
# -----------------------
def fresnel_rt(n1, n2, theta_i):
    theta_i = np.asarray(theta_i, dtype=float)

    sin_t = (n1 / n2) * np.sin(theta_i)
    sin_t = np.clip(sin_t, -1.0, 1.0)
    theta_t = np.arcsin(sin_t)

    cos_i = np.cos(theta_i)
    cos_t = np.cos(theta_t)

    rs = (n1*cos_i - n2*cos_t) / (n1*cos_i + n2*cos_t)
    rp = (n2*cos_i - n1*cos_t) / (n2*cos_i + n1*cos_t)
    ts = (2*n1*cos_i) / (n1*cos_i + n2*cos_t)
    tp = (2*n1*cos_i) / (n2*cos_i + n1*cos_t)

    Rs = np.abs(rs)**2
    Rp = np.abs(rp)**2
    Ts = (n2*cos_t/(n1*cos_i)) * np.abs(ts)**2
    Tp = (n2*cos_t/(n1*cos_i)) * np.abs(tp)**2

    return Rs, Rp, Ts, Tp, theta_t

def plate_power_coeffs(n1, n2, theta_i):
    Rs12, Rp12, Ts12, Tp12, theta_t = fresnel_rt(n1, n2, theta_i)
    Rs21, Rp21, Ts21, Tp21, _       = fresnel_rt(n2, n1, theta_t)

    Rfront_s, Rfront_p = Rs12, Rp12
    Tplate_s = Ts12 * Ts21
    Tplate_p = Tp12 * Tp21
    return Rfront_s, Rfront_p, Tplate_s, Tplate_p

# Choose refractive indices
n1 = 1.0
n2 = 1.5          # placeholder
# n2 = 1.51469     # BK7 at 632.8 nm (example)

theta = np.deg2rad(angles_deg)
R_s, R_p, T_s, T_p = plate_power_coeffs(n1, n2, theta)

# Physics-based predictions in µW
Ref_H_th  = P_in_uW * R_s
Ref_V_th  = P_in_uW * R_p
Trans_H_th = P_in_uW * T_s
Trans_V_th = P_in_uW * T_p

# -----------------------
# Optional: detector scale + background fits
# -----------------------
def fit_scale_offset(P_pred, P_meas):
    A = np.vstack([P_pred, np.ones_like(P_pred)]).T
    scale, offset = np.linalg.lstsq(A, P_meas, rcond=None)[0]
    return scale, offset

sRH, bRH = fit_scale_offset(Ref_H_th, Ref_H)
sRV, bRV = fit_scale_offset(Ref_V_th, Ref_V)
sTH, bTH = fit_scale_offset(Trans_H_th, Trans_H)
sTV, bTV = fit_scale_offset(Trans_V_th, Trans_V)

Ref_H_fit   = sRH * Ref_H_th   + bRH
Ref_V_fit   = sRV * Ref_V_th   + bRV
Trans_H_fit = sTH * Trans_H_th + bTH
Trans_V_fit = sTV * Trans_V_th + bTV

# -----------------------
# Two-panel comparison + residuals (subplots)
# -----------------------
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].scatter(angles_deg, Ref_H, label="Exp Ref H (µW)", color = 'black')
ax[1].scatter(angles_deg, Ref_V, label="Exp Ref V (µW)", color = 'black')
ax[0].plot(angles_deg, Ref_H, zorder = 1, color = 'black')
ax[1].plot(angles_deg, Ref_V, zorder = 1, color = 'black' )
ax[0].plot(angles_deg, Ref_H_fit, label="Theory (cal) Ref H", color = 'red')
ax[1].plot(angles_deg, Ref_V_fit, label="Theory (cal) Ref V", color = 'red')
ax[0].set_xlabel("Incidence angle (deg)")
ax[0].set_ylabel("Reflected power (µW)")
ax[0].grid(True)
ax[0].legend()

ax[0].scatter(angles_deg, Trans_H, label="Exp Trans H (µW)", color = 'blue')
ax[1].scatter(angles_deg, Trans_V, label="Exp Trans V (µW)", color = 'blue')
ax[0].plot(angles_deg, Trans_H, zorder = 1, color = 'blue')
ax[1].plot(angles_deg, Trans_V, zorder = 1, color = 'blue')
ax[0].plot(angles_deg, Trans_H_fit, label="Theory (cal) Trans H", color = 'green')
ax[1].plot(angles_deg, Trans_V_fit, label="Theory (cal) Trans V", color = 'green')
ax[1].set_xlabel("Incidence angle (deg)")
ax[1].set_ylabel("Transmitted power (µW)")
ax[1].grid(True)
ax[1].legend()

fig.suptitle(f"Brewster comparison (n2={n2:.5f})")
fig.tight_layout()

