# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 18:41:02 2026

@author: brian green
"""

#%%
import numpy as np 

price = np.array([8945., 7852., 5999., 4300., 3498., 3598., 3598., 1100., 3165., 22299.], dtype = np.float64)

mark_up_percentage = np.longdouble(135/100)

marked_up_price = np.float64(mark_up_percentage * price)

quantity_of_goods = np. array([2, 2, 2, 2, 15, 10, 20, 80, 2, 1], dtype = np.float64 )

total = np.float64(quantity_of_goods * marked_up_price)

net_total = np.longdouble(sum(total))

profit = net_total * np.longdouble(35/100)

cost_of_goods = sum((price* quantity_of_goods))

total_profit = profit * np.longdouble(95/100)
