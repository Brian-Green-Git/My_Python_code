# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 15:36:21 2026

@author: brian green
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Fetching data
df = pd.read_csv(r"C:\Users\brian green\Desktop\Python\Python\Beam_profiling_results_01.csv")

#%%
class IndependentClean:
    def __init__(self, df):
        # Dropping all the NAN values in the Dataframes 
        
        self.df1 = df[['Position_01', 'Intensity_01']].dropna()
        self.df2 = df[['Position_02', 'Intensity_02']].dropna()
        self.df3 = df[['Position_03', 'Intensity_03']].dropna()
        self.df4 = df[['Position_04', 'Intensity_04']].dropna()
        self.df5 = df[['Position_05', 'Intensity_05']].dropna()
        self.df6 = df[['Position_06', 'Intensity_06']].dropna()
        self.df7 = df[['Position_07', 'Intensity_07']].dropna()
        self.df8 = df[['Position_08', 'Intensity_08']].dropna()
        self.df9 = df[['Position_09', 'Intensity_09']].dropna()
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

#%% Filling nan values 
df = df.fillna(0) 

#%% Cleaning
df = df.drop_duplicates() 

# Filter out and Replace unwanted values with NaN
# Can edit the replace values to remove unwanted values from the Dataframe
df = df.replace([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5], np.nan) 

# Dropping Nan values
cleaned = Recombine(df)

#%% Recombining Data cleaned data 
final_df = cleaned.combined()

#%% Plotting pos < 10 

# PLotting each second graph before focal length
for i in range (1, 10, 2):
    plt.figure()
    plt.plot(final_df["Position_0"+ str(i)], final_df["Intensity_0"+ str(i)], color = "red", linestyle='--')
    plt.scatter(final_df["Position_0"+ str(i)], final_df["Intensity_0"+ str(i)], color = "cyan", zorder = 2)
    plt.xlabel("Position_0" + str(i))
    plt.ylabel("Intensity_0"+ str(i))
    plt.title("Intensity_0"+ str(i) + " VS Position_0" + str(i))
    plt.show()
 
#%% Plotting pos < 10 

# Plotting each second graph after the focal point
for i in range (10, 21, 2):
    plt.figure()
    plt.plot(final_df["Position_"+ str(i)], final_df["Intensity_"+ str(i)], color = "red", linestyle='--')
    plt.scatter(final_df["Position_"+ str(i)], final_df["Intensity_"+ str(i)], color = "cyan", zorder = 2)
    plt.xlabel("Position_" + str(i))
    plt.ylabel("Intensity_"+ str(i))
    plt.title("Intensity_"+ str(i) + " VS Position_" + str(i))
    plt.show()
















