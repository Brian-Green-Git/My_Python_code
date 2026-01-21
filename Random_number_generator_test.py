import numpy as np
import matplotlib.pyplot as plt


#%%

def random_number_generator():
    x = np.random.randint(1, 37, 5)
    return(x) 

values = np.arange(1, 37, 1)

container = np.zeros(36)


def eliminate():
    big = 0

    for i in range(0, 36):
              
        if container[i] < big:
            big = container[i]
    biggest = big
    return biggest


def checkvals(inputval):
    for i in range(0, 5):
       
        for x in range(0, 36):
            if inputval[i] == values[x]:
                container[x] = container[x]+1
    large = eliminate()
    return large
        
for i in range(0,10):
    
    numbers = random_number_generator()
    z = checkvals(numbers)



plt.figure()

# plt.hist(container, bins = 10, density = True)
plt.scatter(values, container, color = "blue")
plt.xlabel("value")
plt.ylabel("probability density")

plt.show()
print(z)
