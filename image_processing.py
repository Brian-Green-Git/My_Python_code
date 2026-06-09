# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:00:39 2026

@author: Photonics LAB
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as Image
import pandas as pd

#%%

location = r"C:\Users\Photonics LAB\Documents\SLM Test Images\Super Positions\02.jpg"

#%%

initial_image = np.array(Image.open(location))[:,:]

#filtering background noise
initial_image[initial_image < 100] = 0

initial_image = initial_image/255

cropped_image = initial_image[750:1300, 650:1225]

# plt.grid(visible = True)
plt.imshow(cropped_image)







