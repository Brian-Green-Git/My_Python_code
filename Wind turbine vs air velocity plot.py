# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 19:11:05 2026

@author: Photonics LAB
"""

import numpy as np
import matplotlib.pyplot as plt


def func(radius, velocity, rho):
    return 1/2*np.pi*rho*radius**2*velocity**3

velocities = np.arange(0, 15, 1)
rad = 10
Rho = 1.225

power = func(rad, velocities, Rho)
power = power/1000

plt.figure()
plt.plot(velocities, power)
plt.xlabel('velocity')
plt.ylabel('power (kw)')
plt.show() 
