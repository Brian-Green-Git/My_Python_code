# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 13:45:41 2026

@author: brian green
"""

#%%
import numpy as np
def array_modifier(lst, value, index):
    
    # 1. Convert the list to a numpy array
    arr = np.array(lst)
    
    # 2. Slice the array into two parts: before the index and after
    part_1 = arr[:index] # everything before index
    part_2 = arr[index:] # everthing after index
    
    # 3. Join them back together with the new value in the middle
    # Note: the value must be wrapped in a list or array to concatenate
    modified_arr = np.concatenate([part_1, [value], part_2])
    
    return modified_arr

    # OR ---------------------------------------
    # arr = np.array(lst)
    # arr2 = np.insert(arr, index, value)
    # return arr2
    
three_dimension = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(three_dimension)

#%%

import numpy as np
def one_dimension_higher(lst):
    arr = np.array(lst)

    return arr

ab = one_dimension_higher([[2, 2,8], [2, 2, None]])

#%%

import numpy as np
def ones_and_zeros(shape):
    zer = np.zeros(shape)
    one = np.ones(shape)

    arr = np.array([zer, one])
    return arr

ones_and_zeros([5,5,5])

#%%

import numpy as np

def dtype_converter(bits, value):
    try:
        if bits == 8:
            return np.array(value+1, dtype=np.int8)
        # Write your code here
        if bits == 16:
            return np.array(value +1, dtype= np.int16)
        if bits == 32:
            return np.array(value +1, dtype= np.int32)
        if bits == 64:
            return np.array(value+1, dtype = np.int64)
    except:
        print("Overflow:", value+1)
        
dtype_converter(16, 32677)
#%%
import numpy as np

arr = np.arange(1, 201, 1)

ary = np.reshape(arr, (20,10))

print(ary)

#%%

import pandas as pd
import numpy as np

a = np.linspace(1,20,20)

z = pd.DataFrame(a, columns = ["fir"])

b = np.linspace(10,29,20)

z["new"] = b

c = np.zeros(20)

z["zerosss"] = c

z["mult"] = np.zeros(20)

for i in range(0, len(z)):

    z.loc[i, "mult"] = z["fir"].iloc[i] * z["new"].iloc[i]

for i in range(0, len(z)):

    z.loc[i, "zerosss"] = z.loc[i, "mult"] * 1.2 * z.loc[i, "new"]

rt = np.array(z)

at = rt * rt

#%%
import numpy as np

# Retrieve the element (using indexing) that contains the value 5 from the 3D array ary
ary = np.array([ [ [ 0, 1 ], [ 2, 3 ] ], [ [ 4, 5 ], [ 6, 7 ] ] ])
print(ary[1,1,0]) 


# Slice [[1,2],[3,4]] and [[9,10], [11,12]] from the ary
# Save the result in the res variable and print res
ary = np.array([ [ [ 1,2 ],[ 3,4 ] ], [ [ 5,6 ],[ 7,8 ] ], [ [ 9,10 ], [ 11,12 ] ] ]) # Don't touch
res = ary[0::2] # <-- Slice
print(str(res).replace('\n', '')) 



# Given a 3D array ary retrieve the 2nd, 3rd and 4th numbers from each 1D array
'''
ary looks like:
array([[[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],

       [[20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]],

       [[40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]],

       [[60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        [70, 71, 72, 73, 74, 75, 76, 77, 78, 79]],

       [[80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
        [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]]])
'''
ary = np.arange(0, 100).reshape(5, 2, 10) 
res = ary[:, : , 1:4:1] 
print(str(res).replace("\n", "")) 

#%%

# Write a function called small_five that receives a list 
# and returns the sum of all elements smaller than 5

import numpy as np

def small_five(lst):

    arr = np.array(lst)
    ary = arr[arr<5]
    return np.sum(ary)
#%%

# Create a function called condition_master that receives a python list
# and returns all the elements that are smaller or equal to 0 or bigger than 5 and not equal to 10.
# Return the result as a python list
# To convert a numpy array to a python list use: str(list(ary))

import numpy as np
def condition_master(lst):

    arr = np.array(lst)
    ary = arr[(arr<= 0) | ((arr>5) & (~(arr == 10)))]
    arry = str(list(ary))
    return arry

#%%

# Create a function called func_operation the receives three python lists
# and returns the sum of ary1 * ary2 / ary3
# Round the result to two decimal places after the dot.
# To round the result use the round method: round(num, 2)

import numpy as np
def func_operation(lst1, lst2, lst3):

    ary1 = np.array(lst1)
    ary2 = np.array(lst2)
    ary3 = np.array(lst3)

    tot = np.sum((ary1*ary2)/ary3)
    tot = np.round(tot, 2)
    return tot

#%%

# Create a function called calculate that receives two python lists, and performs:
# res1 = Subtraction of the two lists
# res2 = Multiplication of the two lists
# and return the dot product of res1 and res2.

import numpy as np
def calculate(lst1, lst2):

    ary1 = np.array(lst1)
    ary2 = np.array(lst2)

    res1 = ary1 - ary2
    res2 = ary1 * ary2

    return(np.dot(res1, res2))
 

   
import sql as sql




















