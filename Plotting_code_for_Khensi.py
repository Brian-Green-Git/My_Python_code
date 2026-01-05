import matplotlib.pyplot as plt
import pandas as pd

#%%

# C:\Users\brian green\Downloads\khensi_forward_data_final.xlsx
# %%

# 16db

# Forward data acquisition 

forward_data_frame = pd.read_excel(r"C:\Users\brian green\Downloads\khensi_forward_data_final.xlsx")

# Reverse data acquisition

backward_data_frame = pd.read_excel(r"C:\Users\brian green\Downloads\khensi_backward_data_final.xlsx")

#%%

# 15db 

# Forward data acquisition 

forward_data_frame_15db = pd.read_excel(r"C:\Users\brian green\Downloads\khensi_forward_data_final_15db.xlsx")

# Reverse data acquisition

backward_data_frame_15db = pd.read_excel(r"C:\Users\brian green\Downloads\khensi_backward_data_final_15db.xlsx")

#%% 

# 5G 

# Forward data acquisition 

forward_data_frame_5g = pd.read_excel(r"C:\Users\brian green\Downloads\khensi_forward_data_final_5g.xlsx")

# Reverse data acquisition

backward_data_frame_5g = pd.read_excel(r"C:\Users\brian green\Downloads\khensi_backward_data_final_5g.xlsx")

#%%
# forward_value_df = forward_data_frame.iloc[:, [1]]
forward_value_df = forward_data_frame["value"]

forward_intensity_df = forward_data_frame["intensity"]

#%%

backward_value_df = backward_data_frame["value"]

backward_intensity_df = backward_data_frame["intensity"]

#%% plotting the data

plt.figure()
plt.rcParams['lines.linewidth'] = 0.8

# plotting the forward data
plt.plot(forward_value_df, forward_intensity_df, label = "16db Forward data")
plt.plot(forward_data_frame_15db["value"], forward_data_frame_15db["intensity"], label = "15db Forward data")
# plt.plot(forward_data_frame_5g["value"], forward_data_frame_5g["intensity"], label = "5G Forward data")

# plotting the backwards data
plt.plot(backward_value_df, backward_intensity_df, label = "16db Reverse data")
plt.plot(backward_data_frame_15db["value"], backward_data_frame_15db["intensity"], label = "15db Reverse data")
# plt.plot(backward_data_frame_5g["value"], backward_data_frame_5g["intensity"], label = "5G Reverse data")

# displaying the plot
plt.xlabel("Magnetic Field [G]")
plt.ylabel("Intensity")
plt.legend()
plt.show()

#%%