# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:37:34 2026

@author: Brian Green
"""
import pandas as pd
import os

for i in range(1, 2):
    #%%
    St_Number = input("Enter Student Number: ")
    Mark = int(input("Enter Mark: "))
     
    #%%
    St = str(St_Number) + "@tut4life.ac.za"
    location = r"C:\Users\Photonics LAB\Downloads\PHYSICS excel\updated_grades.xlsx"
    
    # Read the Excel file
    df = pd.read_excel(location)
    
    # # Debug: Check structure
    # print("=== Debug Information ===")
    # print(f"Looking for student: {St}")
    # print(f"\nTotal rows: {len(df)}")
    # print(f"Column names: {df.columns.tolist()}")
    # print(f"\nFirst few usernames:\n{df['Username'].head()}")
    
    # Check if student exists
    if St in df['Username'].values:
        # Find the student's current mark
        current_mark = df.loc[df['Username'] == St, 'Test 3'].values
        print(f"\nStudent found! Current mark for Test 3: {current_mark[0] if len(current_mark) > 0 else 'Not set'}")
        
        # Update the mark
        df.loc[df['Username'] == St, 'Test 3'] = Mark
        
        # Verify the update
        updated_mark = df.loc[df['Username'] == St, 'Test 3'].values
        print(f"Updated mark: {updated_mark[0]}")
    else:
        print(f"\nERROR: Student {St} not found! ERROR!!!\n\n")
        # print("Sample of actual usernames in file:")
        # print(df['Username'].head(10).tolist())
    
    
    #%%
     
    # Save the updated file
    save_directory = r"C:\Users\Photonics LAB\Downloads\PHYSICS excel"
    save_path = os.path.join(save_directory, "updated_grades.xlsx")
    
    try:
        os.makedirs(save_directory, exist_ok=True)
        df.to_excel(save_path, index=False)
        print(f"\n✓ File saved successfully at: {save_path}")
        print(f"✓ Updated mark {Mark} for student {St_Number}")
    
    except PermissionError:
        print("Permission denied: Please check if the file is open or if you have write access.")
    except FileNotFoundError:
        print("Invalid path: Please check the directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("Quiting")
    

