# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 15:36:21 2026

@author: brian green
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
class IndependentClean:
    def __init__(self, df):
        self.df1 = df[['Position_01', 'Intensity_01']].dropna()
        self.df2 = df[['Position_02', 'Intensity_02']].dropna()
        self.df3 = df[['Position_03', 'Intensity_03']].dropna()

class Recombine(IndependentClean):
    def __init__(self, df):
        super().__init__(df)

    def combined(self):
        df1 = self.df1.reset_index(drop=True)
        df2 = self.df2.reset_index(drop=True)
        df3 = self.df3.reset_index(drop=True)

        combined_df = pd.concat([df1, df2, df3], axis=1)
        return combined_df
    
#%% Fetching data
df = pd.read_csv(r"C:\Users\brian green\Desktop\2026 PHYSICS\New folder\beam_prof_data.csv")

#%% Filling nan values 
df = df.fillna(0) 

#%% Cleaning
df = df.drop_duplicates() 

# Replace unwanted values with NaN
df = df.replace([0, 0.1], np.nan)

# Dropping Nan values
cleaned = Recombine(df)

#%% Recombining Data cleaned data 
final_df = cleaned.combined()

#%% Plotting 

plt.figure()

plt.plot(final_df["Position_03"], final_df["Intensity_03"], color = "red", linestyle='--')

plt.scatter(final_df["Position_03"], final_df["Intensity_03"], color = "cyan", zorder = 2)

plt.show()
 
 
















